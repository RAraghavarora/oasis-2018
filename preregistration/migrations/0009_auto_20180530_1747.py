# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-30 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0008_auto_20180530_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purpleproseextension',
            name='entry',
            field=models.CharField(max_length=100),
        ),
    ]
