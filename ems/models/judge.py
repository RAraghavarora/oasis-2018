from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from events.models import MainEvent

class Judge(models.Model):
	'''
	Development Notes:
	Does not have level field.
	'''
	name = models.CharField(max_length = 200, default = "")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	
	event = models.ForeignKey(MainEvent)
	
	is_active = models.BooleanField(default=True)
	frozen = models.BooleanField(default=False)
	
	#parameter_instances : ParameterInstance

	def __str__(self):
		return self.user.username