from django.db import models
from django.contrib.auth.models import User


class Teller(models.Model):
    """ The name for this model comes from "bank teller". This model is a "user
        extension" model for the people who will be taking cash and then adding
        it to a person's wallet by scanning their qr_code. Mainly to ensure
        transparency and accountability. """

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    cash_collected = models.BigIntegerField(default=0)
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return "Teller {}".format(self.user.username)
