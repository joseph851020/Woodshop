# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-22 18:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import lumberyard.models


class Migration(migrations.Migration):

    dependencies = [
        ('lumberyard', '0004_auto_20160721_2301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliveryspecs',
            options={'verbose_name': 'DeliverySpecs', 'verbose_name_plural': 'DeliverySpecs'},
        ),
        migrations.AlterModelOptions(
            name='departments',
            options={'verbose_name': 'Departments', 'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterModelOptions(
            name='jobs',
            options={'verbose_name': 'Jobs', 'verbose_name_plural': 'Jobs'},
        ),
        migrations.AlterModelOptions(
            name='tasks',
            options={'verbose_name': 'Tasks', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AddField(
            model_name='jobs',
            name='job_dir',
            field=models.CharField(default='NONE', editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='date_delivery',
            field=models.DateTimeField(default=lumberyard.models.date_plus_30, verbose_name='date delivery'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='date_pitch',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
