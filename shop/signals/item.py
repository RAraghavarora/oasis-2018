import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from shop.models.item import ItemClass
from shop.serializers import ItemClassSerializer


@receiver(post_save, sender=ItemClass)
def itemClassFirebaseUpdate(sender, **kwargs):
    db = firestore.client()
    data = ItemClassSerializer(kwargs["instance"]).data
    collection = db.collection("Stall #{}".format(kwargs["instance"].stall.id))
    collection.document("ItemClass #{}".format(kwargs["instance"].id)).set(data)


@receiver(pre_delete, sender=ItemClass)
def itemClassFirebaseDelete(sender, **kwargs):
    db = firestore.client()
    collection = db.collection("Stall #{}".format(kwargs["instance"].stall.id))
    collection.document("ItemClass #{}".format(kwargs["instance"].id)).delete()
