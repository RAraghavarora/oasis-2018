# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-20 10:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_introevent_trivial_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='introevent',
            name='trivial_field',
        ),
        migrations.RemoveField(
            model_name='introevent',
            name='user',
        ),
    ]