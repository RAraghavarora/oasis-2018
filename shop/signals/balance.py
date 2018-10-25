import json
import time


from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from firebase_admin import firestore

from shop.models.balance import Balance
from shop.serializers import BalanceSerializer


@receiver(post_save, sender=Balance)
def balanceFirebaseUpdate(sender, **kwargs):
    try:
        db = firestore.client()
        data = BalanceSerializer(kwargs["instance"]).data
        if kwargs["instance"].wallet.profile == "S":
            # id_str = "Stall #{}".format(kwargs["instance"].wallet.user.id)
            id_str = str(kwargs["instance"].wallet.user.stall.name)
        elif kwargs["instance"].wallet.profile == "T":
            id_str = "Teller #{}".format(kwargs["instance"].wallet.user.id)
        else:
            id_str = "User #{}".format(kwargs["instance"].wallet.user.id)
        collection = db.collection(id_str)
        collection.document("Balance").set(data)
    except:
        time.sleep(1)
        balanceFirebaseUpdate(sender, **kwargs)


@receiver(pre_delete, sender=Balance)
def balanceFirebaseDelete(sender, **kwargs):
    try:
        db = firestore.client()
        if kwargs["instance"].wallet.profile == "S":
            # id_str = "Stall #{}".format(kwargs["instance"].wallet.user.id)
            id_str = str(kwargs["instance"].wallet.user.stall.name)
        elif kwargs["instance"].wallet.profile == "T":
            id_str = "Teller #{}".format(kwargs["instance"].wallet.user.id)
        else:
            id_str = "User #{}".format(kwargs["instance"].wallet.user.id)
        collection = db.collection(id_str)
        collection.document("Balance").delete()
    except:
        time.sleep(1)
        balanceFirebaseDelete(sender, **kwargs)
