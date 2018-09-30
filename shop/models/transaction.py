from django.db import models
from django.utils import timezone

# Import the Wallet class, for some weird reason saying "Wallet" doesn't work
# here, might be due to circular imports or something weird like that.
from shop.models.wallet import *


class Transaction(models.Model):
	""" Main model for handling transactions of money into and out of the user's
		wallet. """

	TYPES = (
		('buy', 'buy'),
		('add', 'add'),
		('transfer','transfer')
	)

	amount = models.PositiveIntegerField(default=0)
	transfer_from = models.ForeignKey("Wallet", related_name="transfered_out",
										on_delete=models.SET_NULL, null=True)
	transfer_to = models.ForeignKey("Wallet", related_name="transfered_in",
										on_delete=models.SET_NULL, null=True)
	transfer_type = models.CharField(max_length=10, default="buy",
										choices=TYPES, null=True)
	payment_id = models.CharField(null=True, max_length=30, unique=True)
	timestamp = models.DateTimeField(default=timezone.now)
	# order: OrderFragment

	def __str__(self):
		return "{} from {} to {}".format(self.amount, self.transfer_from,
											self.transfer_to)
