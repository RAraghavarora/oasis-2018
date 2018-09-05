# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(IntroReg)
admin.site.register(College)
admin.site.register(EmailGroup)
admin.site.register(Participant)
admin.site.register(Group)
admin.site.register(CheckoutGroup)
admin.site.register(Bitsian)
admin.site.register(PaymentGroup)

