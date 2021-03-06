# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-30 11:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Evaluator', '0033_interviewratingsheet_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalinterview',
            name='rating_sheet',
        ),
        migrations.RemoveField(
            model_name='interview',
            name='rating_sheet',
        ),
        migrations.AddField(
            model_name='interviewratingsheet',
            name='interview',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.Interview'),
        ),
        migrations.AddField(
            model_name='interviewratingsheet',
            name='round_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
