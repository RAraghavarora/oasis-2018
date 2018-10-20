# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from preregistration.models import *

from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class IntroEvent(models.Model):
    user = models.OneToOneField(User, related_name="eventmodel", null=True)
    name = models.CharField(max_length=100,unique=True)
    short_description = models.CharField(blank=True,max_length=140)
    rules = models.CharField(blank=True,max_length=200)
    category = models.ForeignKey('Category', default=3, null=True)
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

#####################       MAIN MODELS       #####################

class MainEvent(models.Model):
    """ All the main events for oasis """
    name = models.CharField(max_length = 100, unique=True)
    content = RichTextField(default='NA')
    appcontent = models.TextField(max_length = 3000, default='NA')
    short_description = models.CharField(blank=True, max_length=140)
    rules = models.CharField(blank=True, max_length=200)
    detail_rules = models.TextField(max_length=1000, default='', null=True, blank=True)
    category = models.ForeignKey('Category', default=1)
    is_kernel = models.BooleanField(default= False)
    icon = models.ImageField(blank=True, upload_to = "icons")
    date = models.CharField(max_length=100, default='TBA')
    time = models.CharField(max_length=100, default='TBA')
    venue = models.CharField(max_length=100, default='TBA')
    min_team_size = models.IntegerField(default = 0)
    max_team_size = models.IntegerField(default = 0)
    min_teams = models.IntegerField(default=0)
    max_teams = models.IntegerField(default=0)
    contact = models.CharField(max_length=140, default='NA')

    def __str__(self):
        return self.name

class MainParticipation(models.Model):
    """ Participation of a particular participant in a particular event """

    event = models.ForeignKey(MainEvent, on_delete=models.CASCADE)
    participant = models.ForeignKey('registrations.Participant',on_delete = models.CASCADE, null=True)
    pcr_approved = models.BooleanField(default = False)
    cr_approved = models.BooleanField(default = False)

    def __str__(self):
        return str(self.event.name) + '-' + str(self.participant.name)

class MainProfShow(models.Model):

    name = models.CharField(max_length=100, unique=True)
    appcontent = models.TextField(max_length = 3000, default = '')
    short_description = models.CharField(blank=True, max_length=140)
    date = models.CharField(max_length=100, default='TBA')
    time = models.CharField(max_length=100, default='TBA')
    venue = models.CharField(max_length=100, default='TBA')
    contact = models.CharField(max_length=140, default='')
    price = models.IntegerField(default=0)
    organization = models.ForeignKey("Organization", null=True, default=None, related_name="shows")

    def __str__(self):
        return self.name + '-prof show'

class MainAttendance(models.Model):

    prof_show = models.ForeignKey(MainProfShow, on_delete=models.CASCADE)
    participant = models.ForeignKey('registrations.Participant',on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    passed_count = models.IntegerField(default=0)
    # bitsian = models.ForeignKey('ems.Bitsian', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.prof_show.name)


class Organization(models.Model):
    """ The model for a club or department. Used in the wallet and for scanning
        tickets for prof shows. Only needs to be made for the required clubs and
        departments but not for all. This is a "user extension" model. """

    name = models.CharField(max_length=50, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    disabled = models.BooleanField(default=False)
    # shows: a foreignkey from the MainProfShow model.

    def __str__(self):
        return self.name
