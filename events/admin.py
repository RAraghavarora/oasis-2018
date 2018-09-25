# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Participation)
admin.site.register(IntroEvent)
admin.site.register(MainParticipation)
admin.site.register(MainEvent)
admin.site.register(MainProfShow)
admin.site.register(MainAttendance)
