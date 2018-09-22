import uuid as uuid_pylib

from django.db import models
from django.contrib.auth import User

from registrations.models import Bitsian, Participant

"""
	NOTE: many methods have been left as stubs and will be implemented soon.
"""

class Wallet(models.Model):
    """ The main model where each (bitsian/participant/stall)'s money for the
		wallet will be stored. The E-wallet model. For stalls it denotes amount
		due to them, this way we can keep the Transaction model's to_wallet
		and not have to make an extra field like to_stall. DRY. """

	PROFILES = (
			('bitsian', 'Bitsian'),
			('participant', 'Participant'),
			('stall', 'Stall')
	)

	user = models.OneToOneField(User, on_delete=models.set_null, null=True)
    uuid = models.UUIDField(default=uuid_pylib.uuid4, editable=false)
    phone = models.BigIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)
    profile = models.CharField(max_length=16, choices=PROFILES)
    timestamp = models.DateTimeField(auto_add_now=True)
	# transferred_in: Transactions
	# transferred_out: Transactions
	# orders: Orders
	# cart: Cart

    def __str__(self):
        text = "{}'s wallet"
        try:
            profile = self.getProfile()
			if not profile:
				raise
			else:
				return text.format(profile.name)
        except:
            return (str(self.uid))

	def getProfile(self):
		try:
	        if self.profile == "bitsian":
				return self.user.bitsian
			elif self.profile == "participant":
				return self.user.participant
			elif self.profile == "stall":
				return self.user.stall
			raise
		except:
			return None


class Balance(models.Models):
	""" There are 4 sources of money for each wallet, and it is essential that
		we keep the 4 sources seperate. SWD money must be refunded while other
		money will be lost at the end (the user SHOULD and will be warned)."""
		swd = models.PositiveIntegerField(default=0)
		cash = models.PositiveIntegerField(default=0)
		instamojo = models.PositiveIntegerField(default=0)
		transfers = models.PositiveIntegerField(default=0)

		def __str__(self):
			return("{}/{}/{}/{}".format(swd, cash, instamojo, transfers))


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


class Order(models.Model):
	""" Each order placed by a user. It's basically a composition of
	OrderFragments which comprise the Order as a whole. Mainly created to
	facilitate the "many stalls, many items" ordering feature. """
	customer = models.ForeignKey("Wallet", on_delete=models.SET_NULL,
									related_name="orders", null=True)
	total = models.PositiveIntegerField(default=self.calculateTotal)
	timestamp = models.DateTimeField(default=timezone.now)
	# fragments: OrderFragments

	def __str__(self):
		return "{} - {}".format(self.customer, self.calculateTotal())

	def calculateTotal(self):
		""" This function is kind of a recursive ladder. Calling this would
			also update all subtotals """
		total = 0
		for fragment in self.fragements.all():
			total += fragment.calculateSubTotal()
		self.total = total
		return total


class OrderFragment(models.Model):
	""" Each constituent part of a larger order, part of the the "many stalls,
	many items" ordering feature. """
	stall = models.ForeignKey("Stall", on_delete=SET_NULL, null=True,
								related_name="orders")
	subtotal = PositiveIntegerField(default=self.calculateSubTotal)
	transaction = models.OneToOneField("Transaction", on_delete=models.set_null,
	 										null=True)
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
		# Coming Soon
		pass


class Stall(models.Model):
    """ A simple model for each stall """
    user = models.OneToOneField(User)
	name = models.CharField(max_length=20, blank=True)
    description = models.TextField(default="", blank=True)
	# menu: ItemClasses
	# orders: OrderFragments

	def __str__(self):
		return self.name


class ItemClass(models.Model):
	""" The template for each unique item. See the doctring in the ItemInstance
		model for more background. """

	SIZES = ()
	COLORS = ()
	TYPE = ()

    name = models.CharField(max_length=20, blank=True)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(default='', blank=True)
	is_combo = models.BooleanField(default=False)
	is_available = models.BooleanField(default=True)
	stock = models.PositiveIntegerField(default=500)
	stall = models.ForeignKey("Stall", related_name="menu", null=True,
								on_delete=models.SET_NULL)
	is_veg = models.BooleanField(default=False)
	size = models.CharField(max_length=10, choices=SIZES, null=True)
	colors = models.CharField(max_length=10, choices=COLORS, null=True)
	TYPE = models.CharField(max_length=20, choices=TYPES, null=True)
	timestamp = models.DateTimeField(default=timezone.now)

	# instances: ItemInstances


class ItemInstance(models.Model):
	""" ORM is a great thing. But the only issue is that it doesn't really
		unleash the full power of OOP, an appreciable enough amount, but not
		everything. Hence this model represents each physical item."""
	class_ = models.ForeignKey("ItemClass", related_name="instances", null=True,
								on_delete=models.SET_NULL)
	uuid = models.UUIDField(default=uuid_pylib.uuid4, editable=false)
	quantity = models.PositiveIntegerField(default=1)
	confirmed = models.BooleanField(default=False)
	cancelled = models.BooleanField(default=False)
	paid = models.BooleanField(default=False)
	received = models.BooleanField(default=False)
	cart = models.ForeignKey("Cart", null=True, on_delete=models.SET_NULL,
								related_name="items")
	order = models.ForeignKey("OrderFragment", null=True, on_delete=models.SET_NULL,
								related_name="items")

	def calculatePrice(self):
		return self.class_.price*quantity


class Cart(models.Model):
	""" A temporary yet persistant storage place where the customer can add and remove items
		from in order to decide on their order. Once satisfied, the customer
		can checkout his/her cart and the contents of the cart will be converted
		into an order and the cart will be emptied. """
	wallet = models.OneToOneField("Wallet", on_delete=models.CASCADE)
	# items: ItemInstances

	def add(self):
		pass

	def remove(self):
		pass

	def checkout(self):
		pass
