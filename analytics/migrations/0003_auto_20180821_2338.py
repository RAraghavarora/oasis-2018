# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_viewtimer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewtimer',
            name='seconds_viewed',
            field=models.FloatField(default=0),
        ),
    ]