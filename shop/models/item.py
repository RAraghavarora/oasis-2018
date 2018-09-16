import uuid as uuid_pylib
from django.db import models
from django.utils import timezone
from shop.models.stall import Stall
from shop.models.order import OrderFragment


class ItemClass(models.Model):
	""" A sort of template for each unique item. """

	SIZES = ()
	COLORS = ()
	TYPES = ()

	name = models.CharField(max_length=20, blank=True)
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
		return "{}-{}-{}-{}".format(self.name, self.size, self.color, self.type)

	# instances: ItemInstances


class ItemInstance(models.Model):
	""" This model represents each physical item (each instance)."""

	itemclass = models.ForeignKey("ItemClass", related_name="instances", null=True,
								on_delete=models.CASCADE)
	uuid = models.UUIDField(default=uuid_pylib.uuid4, editable=False)
	quantity = models.PositiveIntegerField(default=1)
	order = models.ForeignKey("OrderFragment", related_name="items", null=True,
								on_delete=models.CASCADE)

	def __str__(self):
		return self.itemclass.name

	def calculatePrice(self):
		return self.class_.price*self.quantity
