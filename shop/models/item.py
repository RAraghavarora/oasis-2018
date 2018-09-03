import uuid as uuid_pylib
from django.db import models
from shop.models.stall import Stall
from shop.models.order import OrderFragment

class ItemClass(models.Model):
	""" The template for each unique item. See the docstring in the ItemInstance
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

	def __str__(self):
		return self.name

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
	order = models.ForeignKey("OrderFragment", related_name="items", null=True,
								on_delete=models.SET_NULL)

	def __str__(self):
		return self.class_.name

	def calculatePrice(self):
		return self.class_.price*quantity
