# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-23 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20181022_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemclass',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
