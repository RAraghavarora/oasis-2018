# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-18 11:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='introevent',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventmodel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='participation',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participation', to='events.IntroEvent'),
        ),
    ]