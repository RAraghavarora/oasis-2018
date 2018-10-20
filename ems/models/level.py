from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from events.models import MainEvent
from ems.models.team import Team

'''
	Development Notes:
	LevelClass and LevelInstance are combined into one model: Level.
	Level.teams is a ManyToMany field.
'''


class LevelClass(models.Model):
	name = models.CharField(max_length = 100, default = '')
	
	event = models.ForeignKey(MainEvent, related_name = "levels", on_delete = models.CASCADE)
	
	#parameters : ParameterClass
	#instances : LevelInstance

	def __str__(self):
		return self.name


class LevelInstance(models.Model):
	levelclass = models.ForeignKey(LevelClass, related_name = "instances", on_delete = models.CASCADE)
	
	team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name = "levels", null = True)
	
	score = models.PositiveSmallIntegerField(default = 0)
	position = models.PositiveSmallIntegerField(blank = True, null = True)
	
	#parameters : ParameterInstance

	def __str__(self):
		return "{} : {}".format(self.levelclass.name, self.participant.username)