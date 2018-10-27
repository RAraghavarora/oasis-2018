# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-26 22:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_stall_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 26, 22, 22, 50, 721083, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='registration_token',
            field=models.CharField(max_length=500, null=True),
        ),
    ]