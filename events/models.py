# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from preregistration.models import GenParticipant

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class IntroEvent(models.Model):
    #user = models.OneToOneField(User, related_name="eventmodel", null=True)
    name = models.CharField(max_length=100,unique=True)
    short_description = models.CharField(blank=True,max_length=140)
    rules = models.CharField(blank=True,max_length=200)
    category = models.ForeignKey('Category', default=3)
    contact = models.CharField(max_length=140, default='')

    def __str__(self):
        return self.name

class Participation(models.Model):
	event = models.ForeignKey(IntroEvent, related_name="participation" ,on_delete=models.CASCADE)
	participant = models.ForeignKey('preregistration.GenParticipant', on_delete=models.CASCADE, null=True)
	pcr_approved = models.BooleanField(default=False)
	cr_approved = models.BooleanField(default=False)

	def __str__(self):
		return str(self.event.name)+'-'+str(self.participant.name)
