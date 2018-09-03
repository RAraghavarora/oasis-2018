from django.db import models
from shop.models.wallet import Wallet


class Transaction(models.Model):
    """ Main model for handling transactions of money into and out of the user's
        wallet. """

	TYPES = (
		('buy', 'buy'),
		('add', 'add'),
        ('recieve','recieve'),
		('transfer','transfer')
	)

    amount = models.PositiveIntegerField(default=0)
    transfer_from = models.ForeignKey("Wallet", related_name="transfered_out",
                                        on_delete=models.SET_NULL, null=True)
    transfer_to = models.ForeignKey("Wallet", related_name="transfered_in",
                                        on_delete=models.SET_NULL, null=True)
    transfer_type = models.CharField(max_length=10, default="buy",
                                        choices=TYPES, null=True)
    refund_id = models.CharField(default="", max_length=30)
    timestamp = models.DateTimeField(default=timezone.now)
	# order: OrderFragment

    def __str__(self):
		return "{} from {} to {}".format(value, transfer_from, transfer_to)
