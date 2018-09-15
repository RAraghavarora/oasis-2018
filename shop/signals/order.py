import json

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from shop.models.order import Order, OrderFragment
from shop.serializers import OrderSerializer, OrderFragmentSerializer

"""
@receiver(post_save, sender=Order)
def orderFirebaseUpdate(sender, **kwargs):
    db = firestore.client()
    data = OrderSerializer(kwargs["instance"]).data
    col_str = "User #{}".format(kwargs["instance"].customer.user.id)
    collection = db.collection(col_str)
    collection.document("Order #{}".format(kwargs["instance"].id)).set(data)


@receiver(pre_delete, sender=Order)
def orderFirebaseDelete(sender, **kwargs):
    db = firestore.client()
    col_str = "User #{}".format(kwargs["instance"].customer.user.id)
    collection = db.collection(col_str)
    collection.document("Order #{}".format(kwargs["instance"].id)).delete()
"""

@receiver(post_save, sender=OrderFragment)
def orderFragmentFoodFirebaseUpdate(sender, **kwargs):
    db = firestore.client()
    data = OrderFragmentFoodSerializer(kwargs["instance"]).data
    col_str = "User #{}".format(kwargs["instance"].stall.id)
    collection = db.collection(col_str)
    doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
    collection.document(doc_string).set(data)


@receiver(pre_delete, sender=OrderFragment)
def orderFragmentFoodFirebaseDelete(sender, **kwargs):
    db = firestore.client()
    col_str = "User #{}".format(kwargs["instance"].stall.id)
    collection = db.collection(col_str)
    doc_string = "OrderFragment #{}".format(kwargs["instance"].id)
    collection.document(doc_string).delete()
