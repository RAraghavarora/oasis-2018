# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-03 08:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0002_auto_20180826_0153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='ems_code',
        ),
    ]
