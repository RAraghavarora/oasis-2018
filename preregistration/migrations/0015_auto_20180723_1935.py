# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0014_auto_20180603_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purpleproseextension',
            name='entry',
            field=models.CharField(max_length=300),
        ),
    ]