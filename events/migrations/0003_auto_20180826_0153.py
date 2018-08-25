# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-25 20:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0002_auto_20180826_0153'),
        ('events', '0002_mainattendance_mainevent_mainparticipation_mainprofshow'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainparticipation',
            name='participant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registrations.Participant'),
        ),
        migrations.AddField(
            model_name='mainevent',
            name='category',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='events.Category'),
        ),
        migrations.AddField(
            model_name='mainattendance',
            name='participant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registrations.Participant'),
        ),
        migrations.AddField(
            model_name='mainattendance',
            name='prof_show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.MainProfShow'),
        ),
    ]
