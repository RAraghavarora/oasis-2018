import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from shop.models.wallet import Wallet

"""
@receiver(post_save, sender=Wallet)
def walletFirebaseUpdate(sender, **kwargs):
    pass


@receiver(pre_delete, sender=Wallet)
def walletFirebaseDelete(sender, **kwargs):
    pass
"""
