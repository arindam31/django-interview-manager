# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-06 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Evaluator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=True, verbose_name='Correct'),
        ),
    ]
