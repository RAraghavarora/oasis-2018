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
	return 'user_{0}/{1}'.format(instance, filename) #instance_user_id

class PaymentGroup(models.Model):
	amount_paid = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now = True)

class EmailGroup(models.Model):
	created_time = models.DateTimeField(auto_now=True)

class Participant(models.Model):

	GENDERS = (
		('M','Male'),
		('F','Female'),
		('O','Others')
		)

	name = models.CharField(max_length=200)
	gender = models.CharField(max_length=10, choices=GENDERS)
	city = models.CharField(max_length=100, null=True)
	email = models.EmailField(unique=True)
	college = models.ForeignKey(College, on_delete=None, null=True)
	phone = models.BigIntegerField()
	barcode = models.CharField(max_length=200, null=True)
	state = models.CharField(max_length=50)
	year_of_study = models.CharField(max_length=3, null=True)
	user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
	#profile_pic = models.ImageField(upload_to=user_directory_path, null=True)
	#verify_docs = models.ImageField(upload_to=user_directory_path, null=True, default=None)
	email_token = models.CharField(max_length=32, null=True, blank=True)
	payment_group = models.ForeignKey(PaymentGroup, on_delete=models.SET_NULL, null=True)
	email_group = models.ForeignKey(EmailGroup, on_delete=models.SET_NULL, null=True)
	group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True)
	# room = models.ForeignKey('regsoft.Room', null=True, blank=True)
	# bill = models.ForeignKey('regsoft.Bill' ,null=True, on_delete=models.SET_NULL)
	recnacc_time = models.DateTimeField(null=True, auto_now=False)
	events = models.ManyToManyField(MainEvent, through=MainParticipation)
	checkout_group = models.ForeignKey('CheckoutGroup', on_delete=models.SET_NULL, null=True)
	# ems_code = models.CharField(max_length=10, default='', null=True)
	bits_id = models.CharField(max_length=20, null=True, blank=True)
	
	# Boolean fields
	
	head_of_society = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)
	is_cr = models.BooleanField(default=False)
	pcr_approved = models.BooleanField(default=False)
	paid = models.BooleanField(default=False)
	pcr_final = models.BooleanField(default=False)
	firewallz_passed = models.BooleanField(default=False)
	acco = models.BooleanField(default=False)
	controlz = models.BooleanField('controlz passed', default=False)
	controlz_paid = models.BooleanField(default=False)
	curr_paid = models.BooleanField(default=False)
	curr_controlz_paid = models.BooleanField(default=False)
	is_g_leader = models.BooleanField(default=False)
	cr_approved = models.BooleanField(default=False)
	is_guest = models.BooleanField(default=False)


	def __str__(self):
		return (self.name) + ' - ' + str(self.college.name)

class Group(models.Model):

	amount_deduct = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now=True)
	group_code = models.CharField(max_length=100, null=True, blank=True)

class CheckoutGroup(models.Model):

	amount_retained = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now=True)
	group_code = models.CharField(max_length=100, null=True, blank=True)


class Bitsian(models.Model):
	
	long_id = models.CharField(max_length=20, null=True, blank=True)
	name = models.CharField(max_length=50, null=True, blank=True)
	gender = models.CharField(max_length=1, null=True, blank=True)
	email = models.EmailField(null=True)
	barcode = models.CharField(max_length=200, null=True, blank=True, unique=True)
	phone = models.BigIntegerField(default=0, null=True)
	bhawan = models.CharField(max_length=20, null=True, blank=True)
	room_no = models.IntegerField(default=0)
	user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.long_id + ' - '+ self.name