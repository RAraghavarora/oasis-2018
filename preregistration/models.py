# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from multiselectfield import MultiSelectField




# Create your models here.

class Roctaves(models.Model):
	name = models.CharField(max_length=50,default='')
	genre = models.CharField(max_length=50,null=False,default='')
	email_address = models.EmailField(null=False)
	phone = models.CharField(default='' , blank = False, max_length=13)
	number_of_participants=models.IntegerField(default=1)
	elimination_preference=models.CharField(max_length=25)
	entry1=models.CharField(max_length=100,null=False)
	entry2=models.CharField(max_length=100,null=False)
	enteries=models.TextField(max_length=200,null=True)
	def __str__(self):
		return self.name
	