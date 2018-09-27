from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from events.models import MainEvent

class Judge(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	event = models.ForeignKey(MainEvent)
	is_active = models.BooleanField(default=True)
	frozen = models.BooleanField(default=False)
	#parameterinstances : ParameterInstance

	def __str__(self):
		return self.user.username