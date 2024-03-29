# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-18 15:40
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20180826_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainevent',
            name='appcontent',
            field=models.TextField(default='NA', max_length=3000),
        ),
        migrations.AlterField(
            model_name='mainevent',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.Category'),
        ),
        migrations.AlterField(
            model_name='mainevent',
            name='contact',
            field=models.CharField(default='NA', max_length=140),
        ),
        migrations.AlterField(
            model_name='mainevent',
            name='content',
            field=ckeditor.fields.RichTextField(default='NA'),
        ),
    ]
