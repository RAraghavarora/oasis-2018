from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from events.models import MainEvent


class LevelClass(models.Model):
	name = models.CharField(max_length = 100)
	event = models.ForeignKey(MainEvent, related_name = "levels", on_delete = models.CASCADE)
	#parameters : ParameterClass
	#instances : LevelInstance

	def __str__(self):
		return self.name


class LevelInstance(models.Model):
	levelclass = models.ForeignKey(LevelClass, related_name = "instances", on_delete = models.CASCADE)
	participant = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	#parameters : ParameterInstance

	def __str__(self):
		return "{} : {}".format(self.levelclass.name, self.participant.username)