import json

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from rest_framework.renderers import JSONRenderer

import firebase_admin
from firebase_admin import credentials, firestore

from shop.models.order import Order, OrderFragment


@receiver(post_save, sender=Order)
def orderFirebaseUpdate(sender, **kwargs):
    pass


@receiver(pre_delete, sender=Order)
def orderFirebaseDelete(sender, **kwargs):
    pass


@receiver(post_save, sender=OrderFragment)
def orderFragmentFirebaseUpdate(sender, **kwargs):
    pass


@receiver(pre_delete, sender=OrderFragment)
def orderFragmentFirebaseDelete(sender, **kwargs):
    pass
