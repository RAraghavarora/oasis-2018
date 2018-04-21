# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Participation, IntroEvent

admin.site.register(Category)
admin.site.register(Participation)
admin.site.register(IntroEvent)
