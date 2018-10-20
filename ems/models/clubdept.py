from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from events.models import MainEvent
from registrations.models import Bitsian


class ClubDepartment(models.Model):
	'''
	Development Notes:
	Does not have email_id field.
	'''

	name = models.CharField(max_length = 100)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	
	coordinator = models.OneToOneField(Bitsian, blank = True)
	
	events = models.ManyToManyField(MainEvent, related_name = "clubdept_event", blank = True)
	profshows = models.ManyToManyField(MainEvent, related_name = "clubdept_prof_show", blank = True)

	mobile = models.PositiveIntegerField(default = 0, blank = True)

	def __str__(self):
		return self.name
