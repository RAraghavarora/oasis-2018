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

	def __str__(self):
		return (self.name)

class IntroReg(models.Model):

	college = models.ForeignKey(College, on_delete = models.CASCADE)
	email_id = models.EmailField(unique=True)
	name = models.CharField(max_length=200)
	mobile_no = models.BigIntegerField()

	def __unicode__(self):
		return str(self.name)+' - '+str(self.college)

	def __str__(self):
		return str(self.name)+' - '+str(self.college)

#####################      MAIN MODELS       #######################

def user_directory_path(instance, filename):
	return 'user_{0}/{1}'.format(instance_user_id, filename)

class PaymentGroup(models.Model):
	amount_paid = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now = True)

class 