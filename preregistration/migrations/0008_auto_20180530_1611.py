# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-30 10:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0007_auto_20180530_1605'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purpleproseextension',
            old_name='yearandstreamofstudy',
            new_name='year_and_stream_of_study',
        ),
    ]
