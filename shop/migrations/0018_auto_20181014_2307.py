# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-14 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_teller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='profile',
            field=models.CharField(choices=[('B', 'bitsian'), ('P', 'participant'), ('S', 'stall'), ('T', 'teller')], max_length=1),
        ),
    ]