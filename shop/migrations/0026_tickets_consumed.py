# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-24 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_debuginfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='consumed',
            field=models.SmallIntegerField(blank=True, default=0),
        ),
    ]