# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Django imports
from django.db import models
from events.models import *
from django.contrib.auth.models import User
#Other imports
from datetime import datetime

#---Models---#

class College(models.Model):

	name = models.CharField(max_length=200, unique=True)

	def __unicode__(self):
		return str(self.name)

class IntroReg(models.Model):

	college = models.ForeignKey(College, on_delete = models.CASCADE)
	email_id = models.EmailField(unique=True)
	name = models.CharField(max_length=200)
	mobile_no = models.BigIntegerField()

	def __unicode__(self):

		return "Name: {}; College: {}".format(str(self.name) + ' ' + str(self.college))
