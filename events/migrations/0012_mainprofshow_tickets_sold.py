# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-24 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20181024_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainprofshow',
            name='tickets_sold',
            field=models.IntegerField(default=0),
        ),
    ]
