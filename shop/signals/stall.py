import json

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

from shop.models.stall import Stall


@receiver(post_save, sender=Stall)
def stallFirebaseUpdate(sender, **kwargs):
    pass


@receiver(pre_delete, sender=Stall)
def stallFirebaseDelete(sender, **kwargs):
    pass
