# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-21 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0003_auto_20180421_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roctaves',
            name='elimination_preference',
            field=models.CharField(max_length=25),
        ),
    ]
