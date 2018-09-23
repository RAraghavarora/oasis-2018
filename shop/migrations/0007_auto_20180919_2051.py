# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-19 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20180916_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderfragment',
            name='status',
            field=models.CharField(choices=[('P', 'pending'), ('F', 'finished'), ('D', 'declined')], default='P', max_length=1),
        ),
    ]