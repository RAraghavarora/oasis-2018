from __future__ import unicode_literals

from django.db import models

class Bhavan(models.Model):

	name = models.CharField(max_length=30)

	def __str__(self):

		return self.name

class Room(models.Model):

	bhavan = models.ForeignKey(Bhavan, on_delete=models.CASCADE)
	room = models.CharField(max_length=30)
	vacancy = models.IntegerField(default=0)
	capacity = models.IntegerField(default=0)

	def __str__(self):

		return self.room + '-' + str(self.bhavan.name)

class Bill(models.Model):

	amount = models.IntegerField()
	time_paid = models.DateTimeField(auto_now=True)
	two_thousands = models.IntegerField(null=True, blank=True, default=0)
	five_hundreds = models.IntegerField(null=True, blank=True, default=0)
	two_hundreds = models.IntegerField(null=True, blank=True, default=0)
	hundreds = models.IntegerField(null=True, blank=True, default=0)
	fifties = models.IntegerField(null=True, blank=True, default=0)
	twenties = models.IntegerField(null=True, blank=True, default=0)
	tens = models.IntegerField(null=True, blank=True, default=0)
	draft_number = models.CharField(max_length=100, null=True, blank=True, default=None)
	draft_amount = models.IntegerField(null=True, blank=True, default=0)
	two_thousands_returned = models.IntegerField(null=True, blank=True, default=0)
	five_hundreds_returned = models.IntegerField(null=True, blank=True, default=0)
	two_hundreds_returned = models.IntegerField(null=True, blank=True, default=0)
	hundreds_returned = models.IntegerField(null=True, blank=True, default=0)
	fifties_returned = models.IntegerField(null=True, blank=True, default=0)
	twenties_returned = models.IntegerField(null=True, blank=True, default=0)
	tens_returned = models.IntegerField(null=True, blank=True, default=0)
	coaches_list = models.CharField(max_length=200, null=True, blank=True)

class Note(models.Model):

	time = models.DateTimeField(auto_now=True, null=True)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	note = models.CharField(max_length=100)

# ***************************** INVENTORY MODELS *************************************


class Location(models.Model):
	name = models.CharField(max_length = 30)
	tender = models.BooleanField(default = True)

	def __str__(self):
		return self.name

class DC(models.Model):
	name = models.CharField(max_length = 30)
	uniqueid = models.CharField(max_length = 10, null = True, blank = True)
	cord = models.CharField(max_length = 30, null = True, blank = True)

	def __str__(self):
		return self.name

class Inventory(models.Model):
	location = models.ForeignKey('Location')
	comments = models.CharField(max_length = 500, null = True, blank = True)
	blankets = models.IntegerField(default = 0, null = True, blank = True)
	mattress = models.IntegerField(default = 0, null = True, blank = True)
	pillows = models.IntegerField(default = 0, null = True, blank = True)
	spikes = models.IntegerField(default = 0, null = True, blank = True)
	bedsheets = models.IntegerField(default = 0, null = True, blank = True)
	quilts = models.IntegerField(default = 0, null = True, blank = True)
	buckets = models.IntegerField(default = 0, null = True, blank = True)
	mugs = models.IntegerField(default = 0, null = True, blank = True)
	fans = models.IntegerField(default = 0, null = True, blank = True)
	bulbs = models.IntegerField(default = 0, null = True, blank = True)
	water_campers = models.IntegerField(default = 0, null = True, blank = True)
	water_drums = models.IntegerField(default = 0, null = True, blank = True)
	waste_drums = models.IntegerField(default = 0, null = True, blank = True)
	tables = models.IntegerField(default = 0, null = True, blank = True)
	table_cloths = models.IntegerField(default = 0, null = True, blank = True)
	chairs = models.IntegerField(default = 0, null = True, blank = True)
	red_carpets = models.IntegerField(default = 0, null = True, blank = True)
	green_carpets = models.IntegerField(default = 0, null = True, blank = True)
	curtains = models.IntegerField(default = 0, null = True, blank = True)
	halogen_lamps = models.IntegerField(default = 0, null = True, blank = True)
	sodium_lamps = models.IntegerField(default = 0, null = True, blank = True)
	tents = models.IntegerField(default = 0, null = True, blank = True)
	iron_poles = models.IntegerField(default = 0, null = True, blank = True)
	paper_rolls = models.IntegerField(default = 0, null = True, blank = True)
	bamboo_poles = models.IntegerField(default = 0, null = True, blank = True)
	ropes = models.IntegerField(default = 0, null = True, blank = True)
	wires = models.IntegerField(default = 0, null = True, blank = True)
	item1 = models.IntegerField(default = 0, null = True, blank = True)
	item2 = models.IntegerField(default = 0, null = True, blank = True)
	item3 = models.IntegerField(default = 0, null = True, blank = True)
	item4 = models.IntegerField(default = 0, null = True, blank = True)
	item5 = models.IntegerField(default = 0, null = True, blank = True)

	def __str__(self):
		return self.location.name


class DC_Inventory(models.Model):
	dc = models.ForeignKey('DC')
	comments = models.CharField(max_length = 500, null = True, blank = True)
	blankets = models.IntegerField(default = 0, null = True, blank = True)
	mattress = models.IntegerField(default = 0, null = True, blank = True)
	pillows = models.IntegerField(default = 0, null = True, blank = True)
	spikes = models.IntegerField(default = 0, null = True, blank = True)
	bedsheets = models.IntegerField(default = 0, null = True, blank = True)
	quilts = models.IntegerField(default = 0, null = True, blank = True)
	buckets = models.IntegerField(default = 0, null = True, blank = True)
	mugs = models.IntegerField(default = 0, null = True, blank = True)
	fans = models.IntegerField(default = 0, null = True, blank = True)
	bulbs = models.IntegerField(default = 0, null = True, blank = True)
	water_campers = models.IntegerField(default = 0, null = True, blank = True)
	water_drums = models.IntegerField(default = 0, null = True, blank = True)
	waste_drums = models.IntegerField(default = 0, null = True, blank = True)
	tables = models.IntegerField(default = 0, null = True, blank = True)
	table_cloths = models.IntegerField(default = 0, null = True, blank = True)
	chairs = models.IntegerField(default = 0, null = True, blank = True)
	red_carpets = models.IntegerField(default = 0, null = True, blank = True)
	green_carpets = models.IntegerField(default = 0, null = True, blank = True)
	curtains = models.IntegerField(default = 0, null = True, blank = True)
	halogen_lamps = models.IntegerField(default = 0, null = True, blank = True)
	sodium_lamps = models.IntegerField(default = 0, null = True, blank = True)
	tents = models.IntegerField(default = 0, null = True, blank = True)
	iron_poles = models.IntegerField(default = 0, null = True, blank = True)
	paper_rolls = models.IntegerField(default = 0, null = True, blank = True)
	bamboo_poles = models.IntegerField(default = 0, null = True, blank = True)
	ropes = models.IntegerField(default = 0, null = True, blank = True)
	wires = models.IntegerField(default = 0, null = True, blank = True)
	item1 = models.IntegerField(default = 0, null = True, blank = True)
	item2 = models.IntegerField(default = 0, null = True, blank = True)
	item3 = models.IntegerField(default = 0, null = True, blank = True)
	item4 = models.IntegerField(default = 0, null = True, blank = True)
	item5 = models.IntegerField(default = 0, null = True, blank = True)

	def __str__(self):
		return self.dc.name
