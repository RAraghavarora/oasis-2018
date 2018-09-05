import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from shop.models.item import ItemClass, ItemInstance


@receiver(post_save, sender=ItemClass)
def itemClassFirebaseUpdate(sender, **kwargs):
    pass


@receiver(pre_delete, sender=ItemClass)
def itemClassFirebaseDelete(sender, **kwargs):
    pass


@receiver(post_save, sender=ItemInstance)
def itemInstanceFirebaseUpdate(sender, **kwargs):
    pass


@receiver(pre_delete, sender=ItemInstance)
def itemInstanceFirebaseDelete(sender, **kwargs):
    pass
