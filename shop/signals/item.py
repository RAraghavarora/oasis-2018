import json
import time

from oasis2018 import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from utils.firestore_issue_mail import send_mail
from shop.models.item import ItemClass
from shop.serializers import ItemClassSerializer


@receiver(post_save, sender=ItemClass)
def itemClassFirebaseUpdate(sender, **kwargs):
    try:
        db = firestore.client()
        data = ItemClassSerializer(kwargs["instance"]).data
        #collection = db.collection("Stall #{}".format(kwargs["instance"].stall.user.id))
        collection = db.collection("Stall #{}".format(kwargs["instance"].stall.user.id))
        collection.document("ItemClass #{}".format(kwargs["instance"].id)).set(data)
    except Exception as e:
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            itemClassFirebaseUpdate(sender, **kwargs)
        elif settings.SERVER:
            send_mail(e, "ItemClass", "Update", ItemClassSerializer(kwargs["instance"]).data)


@receiver(pre_delete, sender=ItemClass)
def itemClassFirebaseDelete(sender, **kwargs):
    try:
        db = firestore.client()
        #collection = db.collection("Stall #{}".format(kwargs["instance"].stall.user.id))
        collection = db.collection(str(kwargs["instance"].stall.name))
        collection.document("ItemClass #{}".format(kwargs["instance"].id)).delete()
    except Exception as e:
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            itemClassFirebaseUpdate(sender, **kwargs)
        elif settings.SERVER:
            send_mail(e, "ItemClass", "Delete", ItemClassSerializer(kwargs["instance"]).data)
