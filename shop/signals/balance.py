import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from shop.models.balance import Balance
from shop.serializers import BalanceSerializer
from signals.firebase_init import getFirestoreDatabase


@receiver(post_save, sender=Balance)
def balanceFirebaseUpdate(sender, **kwargs):
    db = getFirestoreDatabase()
    user = instance.wallet.user
    data = BalanceSerializer(instance).data
    print(data)
    db.collection(user.id).document("Balance").set(data)


@receiver(pre_delete, sender=Balance)
def balanceFirebaseDelete(sender, **kwargs):
    db = getFirestoreDatabase()
    user = instance.wallet.user
    db.collection(user.id).document("Balance").delete()
    pass
