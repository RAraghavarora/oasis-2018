# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-24 10:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regsoft', '0002_auto_20181023_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='table_cloth',
            new_name='table_cloths',
        ),
    ]
