import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from shop.models.wallet import Wallet
from shop.serializers import WalletSerializer


@receiver(post_save, sender=Wallet)
def walletFirebaseUpdate(sender, **kwargs):
    db = firestore.client()
    data = WalletSerializer(kwargs["instance"]).data
    collection = db.collection("User #{}".format(kwargs["instance"].user.id))
    collection.document("Wallet").set(data)


@receiver(pre_delete, sender=Wallet)
def walletFirebaseDelete(sender, **kwargs):
    db = firestore.client()
    collection = db.collection("User #{}".format(kwargs["instance"].user.id))
    collection.document("Wallet").delete()
