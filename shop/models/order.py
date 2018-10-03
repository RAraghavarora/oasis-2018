import json

from django.db import models
from django.utils import timezone
from shop.models.stall import Stall
from shop.models.wallet import Wallet
from shop.models.transaction import Transaction


class Order(models.Model):
	""" Each order placed by a user. It's basically a composition of
	OrderFragments which comprise the Order as a whole. Mainly created to
	facilitate the "many stalls, many items" ordering feature. """

	customer = models.ForeignKey("Wallet", related_name="orders", null=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	query_string = models.TextField(null=True, blank=True) # something extra for the frontend team
	# fragments: OrderFragments

	def __str__(self):
		return "Order : #{} - Customer : {}".format(self.id, self.customer)

	def calculateTotal(self):
		""" This function is kind of a recursive ladder. Calling this would
			also update all subtotals. """
		total = 0
		for fragment in self.fragments.all():
			total += fragment.calculateSubTotal()
		self.total = total
		return total

	def getStatus(self):
		status = {}
		for fragment in self.fragments.all():
			status[fragment.stall] = fragment.status
		return status

	def setQueryString(self, dictionary):
		try:
			self.query_string = json.dumps(dictionary)
			self.save()
			return True
		except Exception as e:
			return False

	def getQueryString(self):
		return json.loads(self.query_string)



class OrderFragment(models.Model):
	""" Each constituent part of a larger order, part of the the "many stalls,
	many items" ordering feature. The order for each stall """

	PENDING = 'P'
	ACCEPTED = 'A'
	DECLINED = 'D'
	FINISHED = 'F'

	STATUS = (
		(PENDING, "Pending"),
		(ACCEPTED, "Accepted"),
		(DECLINED, "Declined"),
		(FINISHED, "Finished") # order is ready for pick-up
	)

	stall = models.ForeignKey("Stall", related_name="orders", null=True, on_delete=models.CASCADE)
	order = models.ForeignKey("Order", related_name="fragments", null=True, on_delete=models.CASCADE)
	transaction = models.OneToOneField("Transaction", null=True, blank=True, on_delete=models.CASCADE)
	status = models.CharField(max_length=1, choices=STATUS, default='P')
	# items: ItemInstances

	def __str__(self):
		return "Order : #{}#{} - Stall : {} - Status : {}".format(self.order.id, self.id, self.stall.name, self.status)

	def calculateSubTotal(self):
		subtotal = 0
		for item in self.items.all():
			subtotal += item.calculatePrice()
		self.subtotal = subtotal
		return subtotal
