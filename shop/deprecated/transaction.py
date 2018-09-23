import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from shop.models.transaction import Transaction
from shop.serializers import TransactionSerializer


@receiver(post_save, sender=Transaction)
def transactionFirebaseUpdate(sender, **kwargs):
    db = firestore.client()
    data = TransactionSerializer(kwargs["instance"]).data

    id_str = "User #{}".format(kwargs["instance"].transfer_to.user.id)
    collection = db.collection(id_str)
    doc_string = "Transcation #{}".format(kwargs["instance"].id)
    collection.document(doc_string).set(data)

    id_str = "User #{}".format(kwargs["instance"].transfer_from.user.id)
    collection = db.collection(id_str)
    doc_string = "Transcation #{}".format(kwargs["instance"].id)
    collection.document(doc_string).set(data)

@receiver(pre_delete, sender=Transaction)
def transactionFirebaseDelete(sender, **kwargs):
    db = firestore.client()

    id_str = "User #{}".format(kwargs["instance"].transfer_to.user.id)
    collection = db.collection(id_str)
    doc_string = "Transcation #{}".format(kwargs["instance"].id)
    collection.document().delete()

    id_str = "User #{}".format(kwargs["instance"].transfer_from.user.id)
    collection = db.collection(id_str)
    doc_string = "Transcation #{}".format(kwargs["instance"].id)
    collection.document().delete()