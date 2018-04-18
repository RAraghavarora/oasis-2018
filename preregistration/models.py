# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Roctaves(models.Model):
    name = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	phone = models.CharField(default='' , blank = False, max_length=13)
	gender = models.CharField(max_length=6)
	email_address = models.EmailField(unique=True)

    def __str__(self):
        return self.name
        