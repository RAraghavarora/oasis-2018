# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-10 03:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IntroReg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('mobile_no', models.BigIntegerField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrations.College')),
            ],
        ),
    ]
