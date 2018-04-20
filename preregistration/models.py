# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from events import *
from django.db import models

class Participant(models.Model):
	name = models.CharField(max_length=100, null=False)
	city = models.CharField(max_length=100)
	phone = models.CharField(default='' , blank = False, max_length=13)
	gender = models.CharField(max_length=6)
	email_address = models.EmailField(unique=True)

	def __str__(self):
		return self.name
