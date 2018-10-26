import json
import time

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer
from shop.models.stall import Stall
from shop.serializers import StallSerializer
from utils.firestore_issue_mail import send_mail


@receiver(post_save, sender=Stall)
def stallFirebaseUpdate(sender, **kwargs):
    try:
        db = firestore.client()
        data = StallSerializer(kwargs["instance"]).data
        collection = db.collection(str(kwargs["instance"].stall.name))
        collection.document("Meta Data").set(data)
    except Exception as e:
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            stallFirebaseUpdate(sender, **kwargs)
        elif settings.SERVER:
            send_mail(e, "Stall", "Update", StallSerializer(kwargs["instance"]).data)


@receiver(pre_delete, sender=Stall)
def stallFirebaseDelete(sender, **kwargs):
    try:
        db = firestore.client()
        data = StallSerializer(kwargs["instance"]).data
        collection = db.collection(str(kwargs["instance"].stall.name))
        collection.document("Meta Data").delete()
    except Exception as e:
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            stallFirebaseUpdate(sender, **kwargs)
        elif settings.SERVER:
            send_mail(e, "Stall", "Delete", StallSerializer(kwargs["instance"]).data)
