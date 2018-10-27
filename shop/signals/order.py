import json
import time

from oasis2018 import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from utils.firestore_issue_mail import send_mail
from shop.models.order import Order, OrderFragment
from shop.serializers import OrderSerializer, OrderFragmentSerializer


@receiver(post_save, sender=OrderFragment)
def orderFragmentFirebaseUpdate(sender, **kwargs):
    try:
        db = firestore.client()
        data = OrderFragmentSerializer(kwargs["instance"]).data

        col_str = "User #{}".format(kwargs["instance"].order.customer.user.id)
        collection = db.collection(col_str)
        doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
        collection.document(doc_string).set(data)

        # col_str = "Stall #{}".format(kwargs["instance"].stall.user.id)
        col_str = str(kwargs["instance"].stall.user.username)
        collection = db.collection(col_str)
        doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
        collection.document(doc_string).set(data)
    except Exception as e:
        print(e)
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            orderFragmentFirebaseUpdate(sender, **kwargs)
        elif settings.SERVER:
            send_mail(e, "OrderFragment", "Update", OrderFragmentSerializer(kwargs["instance"]).data)


@receiver(pre_delete, sender=OrderFragment)
def orderFragmentFirebaseDelete(sender, **kwargs):
    try:
        db = firestore.client()

        col_str = "User #{}".format(kwargs["instance"].order.customer.user.id)
        collection = db.collection(col_str)
        doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
        collection.document(doc_string).delete()

        #col_str = "Stall #{}".format(kwargs["instance"].stall.user.id)
        col_str = str(kwargs["instance"].stall.user.username)
        collection = db.collection(col_str)
        doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
        collection.document(doc_string).delete()
    except Exception as e:
        print(e)
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            orderFragmentFirebaseDelete(sender, **kwargs)
        elif settings.SERVER:
            send_mail(e, "OrderFragment", "Delete", OrderFragmentSerializer(kwargs["instance"]).data)
