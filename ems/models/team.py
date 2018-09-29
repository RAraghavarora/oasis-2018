from __future__ import unicode_literals

from django.db import models

from events.models import MainEvent
from registrations.models import Participant, Bitsian

class Team(models.Model):

    PARTICIPANT = 'P'
    FINALIST = 'F'
    WINNER = 'W'

    STATUS = (
        (PARTICIPANT, "Participant"),
        (FINALIST, "Finalist"),
        (WINNER, "Winner"),
    )

    name = models.CharField(max_length = 200, default = 'No Name')
    
    members = models.ManyToManyField(Participant)
    leader = models.ForeignKey(Participant, related_name = 'team_leader', null = True)
    
    members_bitsian = models.ManyToManyField(Bitsian)
    leader_bitsian = models.ForeignKey(Bitsian, related_name = 'bitsian_leader', null = True)
    
    event = models.ForeignKey(MainEvent, on_delete = models.CASCADE, null = True)
    score = models.IntegerField(default = 0)
    
    rank = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length = 1, choices = STATUS, default = 'P')

    def __str__(self):
        return self.name