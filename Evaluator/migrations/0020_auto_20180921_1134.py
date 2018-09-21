# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-21 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Evaluator', '0019_auto_20180920_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='result',
            field=models.CharField(choices=[('ADV', 'Advanced'), ('RJ', 'Rejected'), ('CN', 'Cancelled'), ('DNA', 'Did Not Appear'), ('DNO', 'Did Not Accept Offer'), ('RS', 'Rescheduled'), ('W', 'Waiting'), ('S', 'Selected'), ('OH', 'On Hold')], default='W', max_length=5),
        ),
        migrations.AlterField(
            model_name='round',
            name='round_type',
            field=models.CharField(choices=[('U', 'Undecided'), ('F2F', 'Face to Face'), ('SKYPE', 'Skype Call'), ('TP', 'Telephonic'), ('VC', 'Client Video Call'), ('FD', 'Final Discussion'), ('HR', 'HR Discussion'), ('Other', 'Other Types')], default='U', max_length=10),
        ),
    ]
