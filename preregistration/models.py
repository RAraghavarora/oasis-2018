# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from events.models import *

class GenParticipant(models.Model):
	name = models.CharField(max_length=100, null=False)
	city = models.CharField(max_length=100,null=True,default='')
	phone = models.CharField(default='' , blank = False, max_length=13)
	gender = models.CharField(max_length=6,null=True,default='')
	email_address = models.EmailField(null=False, unique=False, default="")
	def __str__(self):
		return self.name


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

# this one is just here for formality
class PoetrySlamExtension(models.Model):
	participant = models.OneToOneField(GenParticipant)

	def __str__(self):
		name = self.participant.name
		name += " - Extension"
		return name

	def getEvent(self):
		try:
			return IntroEvent.objects.get(name="PoetrySlam")
		except:
			return None

class RapWarsExtension(models.Model):
	participant = models.OneToOneField(GenParticipant)
	rapper_name = models.CharField(max_length=100, default="")
	city_of_participation = models.CharField(max_length=30, default="")

	def __str__(self):
		name = self.participant.name
		name += " - Extension"
		return name

	def getEvent(self):
		try:
			return IntroEvent.objects.get(name="RapWars")
		except:
			return None

class PurpleProseExtension(models.Model):
	participant=models.OneToOneField(GenParticipant)
	college=models.CharField(max_length=100,default="")
	year_and_stream_of_study=models.CharField(max_length=100,default="")
	city_of_participation = models.CharField(max_length=30, default="")
	entry=models.CharField(max_length=100,null=False)

	def __str__(self):
		name=self.participant.name
		name+=" - Extension"
		return name
	def getEvent(self):
		try:
			return IntroEvent.orbject.get(name="PurpleProse")
		except:
			return None

class StandupSoapboxExtension(models.Model):
	participant=models.OneToOneField(GenParticipant)
	time_doing_standup=models.CharField(max_length=20,default="",null=False)
	previous_competition=models.TextField(max_length=300,default="")
	def __str__(self):
		name=self.participant.name
		name+=" -Extension"
		return name

	def getEvent(self):
		try:
			return IntroEvent.objects.get(name="StandupSoapbox")
		except:
			return None
