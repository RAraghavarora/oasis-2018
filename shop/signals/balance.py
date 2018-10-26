import json
import time

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from oasis2018 import settings
from firebase_admin import firestore
from utils.firestore_issue_mail import send_mail

from shop.models.balance import Balance
from shop.serializers import BalanceSerializer


@receiver(post_save, sender=Balance)
def balanceFirebaseUpdate(sender, **kwargs):
    try:
        db = firestore.client()
        data = BalanceSerializer(kwargs["instance"]).data
        if kwargs["instance"].wallet.profile == "S":
            id_str = kwargs["instance"].wallet.user.stall.name
        elif kwargs["instance"].wallet.profile == "T":
            id_str = "Teller #{}".format(kwargs["instance"].wallet.user.id)
        else:
            id_str = "User #{}".format(kwargs["instance"].wallet.user.id)
        collection = db.collection(id_str)
        collection.document("Balance").set(data)
    except Exception as e:
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            balanceFirebaseUpdate(sender, **kwargs)
        elif settings.SERVER:
            ### SOME SERIOUS ISSUE HAS OCCURRED WITH FIRESTORE
            send_mail(e, "Balance", "Update", BalanceSerializer(kwargs["instance"]).data)


@receiver(pre_delete, sender=Balance)
def balanceFirebaseDelete(sender, **kwargs):
    try:
        db = firestore.client()
        if kwargs["instance"].wallet.profile == "S":
            id_str = kwargs["instance"].wallet.user.stall.name
        elif kwargs["instance"].wallet.profile == "T":
            id_str = "Teller #{}".format(kwargs["instance"].wallet.user.id)
        else:
            id_str = "User #{}".format(kwargs["instance"].wallet.user.id)
        collection = db.collection(id_str)
        collection.document("Balance").delete()
    except Exception as e:
        time.sleep(1)
        if "iteration" not in kwargs.keys():
            kwargs["iteration"] = 1
        kwargs["iteration"] += 1
        if kwargs["iteration"] < 10:
            balanceFirebaseDelete(sender, **kwargs)
        elif settings.SERVER:
            send_mail(e, "Balance", "Delete", BalanceSerializer(kwargs["instance"]).data)
