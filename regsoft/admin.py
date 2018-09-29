# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(Bhavan)
admin.site.register(Room)
admin.site.register(Bill)
admin.site.register(Note)
