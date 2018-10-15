import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from events.models import MainEvent
from events.serializers import MainEventSerializer

from firebase_admin import firestore


@receiver(post_save, sender=MainEvent)
def mainEventsRealtimeUpdate(sender, **kwargs):
    db = firestore.client()
    data = MainEventSerializer(kwargs["instance"]).data
    collection = db.collection("Events")
    collection.document(data["name"]).set(data)


@receiver(pre_delete, sender=MainEvent)
def mainEventsRealtimeDelete(sender, **kwargs):
    db = firestore.client()
    document_name = kwargs["instance"].name
    collection = db.collection("Events")
    collection.document(document_name).delete()
