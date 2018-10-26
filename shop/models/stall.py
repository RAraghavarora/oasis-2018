from django.db import models
from django.contrib.auth.models import User


class Stall(models.Model):
    """ A simple model for each stall """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20)
    description = models.TextField(default="", blank=True)
    phone = models.BigIntegerField(default=0)
    closed = models.BooleanField(default=False)
	# menu: ItemClasses
	# orders: OrderFragments

    def __str__(self):
        return self.name
