import uuid as uuid_pylib

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from shop.models.stall import Stall
from shop.models.order import OrderFragment
from events.models import MainProfShow


class ItemClass(models.Model):
	""" A sort of template for each unique item. """

	SIZES = ()
	COLORS = ()
	TYPES = ()

	name = models.CharField(max_length=20)
	stall = models.ForeignKey("Stall", related_name="menu", null=True, on_delete=models.CASCADE)
	description = models.TextField(default='', blank=True)
	is_combo = models.BooleanField(default=False)
	is_veg = models.BooleanField(default=False)

	price = models.PositiveIntegerField(default=0)
	is_available = models.BooleanField(default=True)
	stock = models.PositiveIntegerField(default=500)

	size = models.CharField(max_length=10, choices=SIZES, null=True, blank=True)
	color = models.CharField(max_length=10, choices=COLORS, null=True, blank=True)
	itemtype = models.CharField(max_length=20, choices=TYPES, null=True, blank=True)

	timestamp = models.DateTimeField(default=timezone.now)

	def __str__(self):
		ret_string = "Stall : {} - Name : {}".format(self.stall, self.name)

		if self.size:
			ret_string += " - Size : {}".format(self.size)
		elif self.color:
			ret_string += " - Color : {}".format(self.color)
		elif self.itemtype:
			ret_string += " - Itemtype : {}".format(self.itemtype)

		return ret_string

	# instances: ItemInstances


class ItemInstance(models.Model):
	""" This model represents each physical item (each instance)."""

	itemclass = models.ForeignKey("ItemClass", related_name="instances", null=True, on_delete=models.CASCADE)
	uuid = models.UUIDField(default=uuid_pylib.uuid4, editable=False)
	quantity = models.PositiveIntegerField(default=1)
	order = models.ForeignKey("OrderFragment", related_name="items", null=True, on_delete=models.CASCADE)

	def __str__(self):
		return "Order : #{} - ItemName : {}".format(self.order.order.id, self.itemclass.name)

	def calculatePrice(self):
		return self.itemclass.price*self.quantity


class Tickets(models.Model):
	""" A simple through model kind of class for holding tickets to prof shows.
		Each instance represents the number of tickets a particular user has for a
		particular prof show. """

	prof_show = models.ForeignKey(MainProfShow, null=True, on_delete=models.SET_NULL, related_name="tickets")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
	count = models.SmallIntegerField(default=0, blank=True)

	def __str__(self):
		try:
			profile = self.user.bitsian
		except:
			try:
				profile = self.user.participant
			except:
				profile = self.user.id
		return "{}'s tickets for {} : {}".format(profile.name, self.prof_show.name, self.count)

	class Meta:
		verbose_name_plural = "Tickets"
