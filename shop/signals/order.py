import json

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from shop.models.order import Order, OrderFragment
from shop.serializers import OrderSerializer, OrderFragmentSerializer


@receiver(post_save, sender=OrderFragment)
def orderFragmentFirebaseUpdate(sender, **kwargs):
    db = firestore.client()
    data = OrderFragmentSerializer(kwargs["instance"]).data

    col_str = "User #{}".format(kwargs["instance"].order.customer.user.id)
    collection = db.collection(col_str)
    doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
    collection.document(doc_string).set(data)

    # col_str = "Stall #{}".format(kwargs["instance"].stall.user.id)
    col_str = str(kwargs["instance"].stall.name)
    print(kwargs["instance"].stall.user.id)
    collection = db.collection(col_str)
    doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
    collection.document(doc_string).set(data)


@receiver(pre_delete, sender=OrderFragment)
def orderFragmentFirebaseDelete(sender, **kwargs):
    db = firestore.client()

    col_str = "User #{}".format(kwargs["instance"].order.customer.user.id)
    collection = db.collection(col_str)
    doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
    collection.document(doc_string).delete()

    #col_str = "Stall #{}".format(kwargs["instance"].stall.user.id)
    col_str = str(kwargs["instance"].stall.name)
    collection = db.collection(col_str)
    doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
    collection.document(doc_string).delete()
