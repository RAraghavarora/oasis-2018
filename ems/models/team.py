from __future__ import unicode_literals

from django.db import models

from events.models import MainEvent
from registrations.models import Participant, Bitsian

class Team(models.Model):
    '''
    Development Notes:
    Does not have is_winner, is_finalist, level fields.
    Instead has status field.

    '''

    PARTICIPANT = 'P'
    FINALIST = 'F'
    WINNER = 'W'

    STATUS = (
        (PARTICIPANT, "Participant"),
        (FINALIST, "Finalist"),
        (WINNER, "Winner"),
    )

    name = models.CharField(max_length = 200, default = 'No Name')
    
    members = models.ManyToManyField(Participant, blank = True)
    leader = models.ForeignKey(Participant, related_name = 'team_leader', null = True, blank = True)
    
    members_bitsian = models.ManyToManyField(Bitsian, blank = True)
    leader_bitsian = models.ForeignKey(Bitsian, related_name = 'bitsian_leader', null = True, blank = True)
    
    event = models.ForeignKey(MainEvent, on_delete = models.CASCADE, null = True)
    score = models.IntegerField(default = 0, blank = True)
    
    rank = models.PositiveSmallIntegerField(default=0, blank = True)
    status = models.CharField(max_length = 1, choices = STATUS, default = 'P')

    #levels: LevelInstance

    def __str__(self):
        return self.name