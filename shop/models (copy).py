import uuid
from django.db import models
from registrations.models import Bitsian, Participant


class Wallet(models.Model):
    """ The main model where each (bitsian/participant)'s money for the wallet
        will be stored. The E-wallet model. """

    uid = models.UUIDField(default=uuid.uuid4, editable=false)
    user = models.OneToOneField(User, on_delete=models.set_null, null=True)
    phone = models.CharField(default="+910000000000")
    balance = models.PositiveIntegerField(default=0)
    is_bitsian = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__():
        text = "{}'s wallet"
        try:
            if self.is_bitsian:
                return text.format(self.get_bitsian().name)
            elif self.is_participant:
                return text.format(self.get_participant().name)
        except:
            return text.format(self.uid)

    def get_bitsian():
        try:
            return self.user.bitsian
        except:
            return None

    def get_participant():
        try:
            return self.user.participant
        except:
            return None


class Transaction(models.Model):
    """ Main model for handling transactions of money into and out of the user's
        wallet. """

	transaction_coices = (
		('buy', 'buy'),
		('add', 'add'),
        ('recieve','recieve'),
		('transfer','transfer')
	)
    value = models.IntegerField(default=0)
    transfer_from = models.ForeignKey('Wallet', related_name="transfered_out",
                                        on_delete=models.SET_NULL, null=True)
    transfer_to = models.ForeignKey('Wallet', related_name="transfered_in",
                                        on_delete=models.SET_NULL, null=True)
    transfer_type = models.CharField(max_length=10, default='buy',
                                        choices=transaction_coices)
    payment_refund_id = models.CharField(default='', max_length=30)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
		return "{} from {} to {}".format(value, transfer_from, transfer_to)


class Cart(models.Model):
    """ ??? """

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
                                    related_name="carts")
	is_bitsian = models.BooleanField(default=False)
	is_participant = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
	timestamp = models.DateTimeField(default=timezone.now)

	def __str__(self):
        text = "{}'s cart at {}"
        try:
            if self.is_bitsian:
                return text.format(self.get_bitsian().name, self.timestamp)
            elif self.is_participant:
                return text.format(self.get_participant().name, self.timestamp)
        except:
            return text.format(self.user, self.timestamp)

    def get_bitsian():
        try:
            return self.user.bitsian
        except:
            return None

    def get_participant():
        try:
            return self.user.participant
        except:
            return None


class ProductClass(models.Model):
    """ The ORM is quite handy but it's not OOP, so since we can't make certain
        fields like is_available and quantity static variables we need this
        "ProductClass" model and a complementary "ProductInstance" model.  """

	is_available = models.BooleanField(default=True)
	quantity = models.IntegerField(default=500)

    name = models.CharField(max_length=20, blank=True)
    price = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True)

    stall = models.ForeignKey('Stall', related_name="menu", null=True)
    prof_show = models.ForeignKey('events.MainProfShow', null=True)

    # Miscellaneous Data
    is_veg = models.BooleanField(default=False)
    size = models.CharField(maxlength=8, blank=True, null=True)
    color = models.CharField(maxlength=16, blank=True, null=True)
    product_type = models.CharField(maxlength=16, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.name + ' - ' + str(self.product_type)

"""
# Try eliminating this Class
class ProductInstance(models.Model):
    \"\"\" Each induvisual product \"\"\"
	product = models.ForeignKey('ProductClass', on_delete=models.SET_NULL,
                                    null=True, related_name="instances")
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.product)
"""

class Stall(models.Model):
    """ A simple model for each stall """
    user = models.OneToOneField(User)
	name = models.CharField(max_length=20, blank=True)
    description = models.TextField(default="", blank=True)

	def __str__(self):
		return self.name


class StallGroup(models.Model):
    """ It is possible for a person to order multiple items from multiple stalls
        at once. This Model, in a nutshell, allows that to happen. """
	created_at = models.DateTimeField(default=timezone.now)
	is_bitsian = models.BooleanField(default=False)
	bitsian = models.ForeignKey('registrations.Bitsian', on_delete=models.SET_NULL, null=True, related_name="stallgroup")
	stall = models.ForeignKey(Stall, null=True, on_delete=models.SET_NULL)
	sale_group = models.ForeignKey(SaleGroup, null=True, on_delete=models.SET_NULL)
	participant = models.ForeignKey('registrations.Participant', on_delete=models.SET_NULL, null=True)
	amount = models.IntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order_complete = models.BooleanField(default=False)
	group_paid = models.BooleanField(default=False)
	unique_code = models.CharField(max_length=20, default='', null=True)
	transaction = models.OneToOneField('Transaction', null=True, default=None, related_name='stallgroup')
	cancelled = models.BooleanField(default=False)
	code_requested = models.BooleanField(default=False)
	orderid = models.CharField(max_length=20, default='')
	order_ready = models.BooleanField(default=False)


class Item(models.Model):

	is_available = models.BooleanField(default=True)
	quantity = models.IntegerField(default=500)

    name = models.CharField(max_length=20, blank=True)
    price = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True)

    stall = models.ForeignKey('Stall', related_name="menu", null=True) #########
    # prof_show = models.ForeignKey('events.MainProfShow', null=True) make it a seperate mode ==> TICKET.

    # Miscellaneous Data
    is_veg = models.BooleanField(default=False)
    size = models.CharField(maxlength=8, blank=True, null=True)
    color = models.CharField(maxlength=16, blank=True, null=True)
    product_type = models.CharField(maxlength=16, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.name + ' - ' + str(self.product_type)
