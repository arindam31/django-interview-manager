# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-13 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Evaluator', '0046_ratingaspect_expected_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='interviewratingsheet',
            name='comment',
            field=models.TextField(default='', null=True),
        ),
    ]
