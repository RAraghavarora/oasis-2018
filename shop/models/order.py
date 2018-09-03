from django.db import models
from django.utils import timezone
from shop.models.stall import Stall
from shop.models.wallet import Wallet
from shop.models.transaction import Transaction


class Order(models.Model):
	""" Each order placed by a user. It's basically a composition of
	OrderFragments which comprise the Order as a whole. Mainly created to
	facilitate the "many stalls, many items" ordering feature. """
	customer = models.ForeignKey("Wallet", related_name="orders", null=True,
									on_delete=models.SET_NULL)
	timestamp = models.DateTimeField(default=timezone.now)
	# fragments: OrderFragments

	def __str__(self):
		return "{} - {}".format(self.customer, self.calculateTotal())

	def calculateTotal(self):
		""" This function is kind of a recursive ladder. Calling this would
			also update all subtotals. """
		total = 0
		for fragment in self.fragements.all():
			total += fragment.calculateSubTotal()
		self.total = total
		return total


class OrderFragment(models.Model):
	""" Each constituent part of a larger order, part of the the "many stalls,
	many items" ordering feature. """
	stall = models.ForeignKey("Stall", related_name="orders", null=True,
								on_delete=models.SET_NULL)
	transaction = models.OneToOneField("Transaction", null=True,
										on_delete=models.SET_NULL)
	# items: ItemInstances

	def __str__(self):
		return "order: #{} - {}".format(self.calculateSubTotal())

	def calculateSubTotal(self):
		subtotal = 0
		for item in self.items.all():
			subtotal += item.calculatePrice()
		self.subtotal = subtotal
		return subtotal
