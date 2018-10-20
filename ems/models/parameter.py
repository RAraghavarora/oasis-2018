from __future__ import unicode_literals

from django.db import models

from ems.models.judge import Judge
from ems.models.level import LevelClass, LevelInstance


class ParameterClass(models.Model):
	'''
	Development Notes:
	Same as the Parameter model.
	'''
	name = models.CharField(max_length = 100)
	
	level = models.ForeignKey(LevelClass, related_name = "parameters", on_delete = models.CASCADE)
	
	max_value = models.IntegerField(default = 0)
	
	#instances : ParameterInstance

	def __str__(self):
		return self.name


class ParameterInstance(models.Model):
	'''
	Development Notes:
	Same as Score to some extent.
	Does not have score_card and comments, instead has value and comment.
	Also does not have total score, instead there is a score field in levelinstance.
	'''
	parameterclass = models.ForeignKey(ParameterClass, related_name = "instances", on_delete = models.CASCADE)
	
	level = models.ForeignKey(LevelInstance, related_name = "parameters", on_delete = models.CASCADE)
	
	judge = models.ForeignKey(Judge, related_name = "parameter_instances", on_delete = models.CASCADE)
	value = models.IntegerField(default = 0)
	comment = models.CharField(max_length = 500, default = '', blank = True)
	
	def __str__(self):
		ret_string = "Level : {}".format(self.parameterclass.level.name) + \
			" - Parameter : {}".format(self.parameterclass.name) + \
			" - Participant : {}".format(self.level.participant.username)

		return ret_string