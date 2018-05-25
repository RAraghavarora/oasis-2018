# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 04:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='introevent',
            name='category',
            field=models.ForeignKey(default=3, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Category'),
        ),
    ]
