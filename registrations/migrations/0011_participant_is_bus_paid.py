# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-24 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0010_participant_is_chor'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='is_bus_paid',
            field=models.BooleanField(default=False),
        ),
    ]
