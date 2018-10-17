# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-27 13:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_auto_20180918_2110'),
        ('registrations', '0008_auto_20180926_0240'),
        ('ems', '0002_auto_20180927_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.PositiveIntegerField(default=0)),
                ('coordinator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='registrations.Bitsian')),
                ('events', models.ManyToManyField(to='events.MainEvent')),
                ('profshows', models.ManyToManyField(to='events.MainEvent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]