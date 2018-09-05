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
									on_delete=models.CASCADE)
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

	def getStatus(self):
		status = {}
		for fragment in self.fragments.all():
			status[fragment.stall] = fragment.status
		return status

	def generateTransactions(self):
		""" Also, in some ways a recursive ladder of generating Transactions.
			Each OrderFragment will have to generate its own Transaction, which
			in turn involves calling the Transaction model's method(s). """
		for fragment in self.fragments.all():
			fragment.generateTransaction()


class OrderFragment(models.Model):
	""" Each constituent part of a larger order, part of the the "many stalls,
	many items" ordering feature. The order for each stall """

	STATUS = (
		("in-review", "in-review"),
		("accepted", "accepted"),
		("declined", "declined"),
		("finished", "finished"), # order is ready for pick-up
		("completed", "completed"), # order has been paid for and picked up
		("cancelled", "cancelled") # to cancel certain parts
	)

	stall = models.ForeignKey("Stall", related_name="orders", null=True,
								on_delete=models.CASCADE)
	order = models.ForeignKey("Order", related_name="fragments", null=True,
								on_delete=models.CASCADE)
	transaction = models.OneToOneField("Transaction", null=True,
										on_delete=models.CASCADE)
	status = models.CharField(max_length=20, choices=STATUS, default="in-review")
	# items: ItemInstances

	def __str__(self):
		return "order: #{} - {}".format(self.calculateSubTotal())

	def calculateSubTotal(self):
		subtotal = 0
		for item in self.items.all():
			subtotal += item.calculatePrice()
		self.subtotal = subtotal
		return subtotal

	def generateTransaction(self):
		""" To be called by Order's getTransactions method. """
		self.transaction = Transaction.newTransaction("")
