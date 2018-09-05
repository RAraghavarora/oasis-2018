import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from shop.models.transaction import Transaction


@receiver(post_save, sender=Order)
def transactionFirebaseUpdate(sender, **kwargs):
    pass


@receiver(pre_delete, sender=Order)
def transactionFirebaseDelete(sender, **kwargs):
    pass
