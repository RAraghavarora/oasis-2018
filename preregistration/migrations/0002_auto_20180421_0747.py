# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-21 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roctaves',
            old_name='eliminationpreference',
            new_name='elimination_preference',
        ),
        migrations.AddField(
            model_name='roctaves',
            name='enteries',
            field=models.TextField(max_length=200, null=True),
        ),
    ]
