# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-24 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20181016_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainprofshow',
            name='organization',
        ),
        migrations.AddField(
            model_name='mainprofshow',
            name='organization',
            field=models.ManyToManyField(default=None, related_name='shows', to='events.Organization'),
        ),
    ]
