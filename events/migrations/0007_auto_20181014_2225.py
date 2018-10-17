# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-14 16:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20181014_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainevent',
            name='organization',
        ),
        migrations.AddField(
            model_name='mainprofshow',
            name='organization',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Organization'),
        ),
    ]