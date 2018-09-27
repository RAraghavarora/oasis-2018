from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from events.models import MainEvent
from registrations.models import Bitsian


class ClubDepartment(models.Model):
	name = models.CharField(max_length = 100)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	
	coordinator = models.OneToOneField(Bitsian)
	
	events = models.ManyToManyField(MainEvent)
	profshows = models.ManyToManyField(MainEvent)

	mobile = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return self.name
