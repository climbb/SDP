# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enrollment', '0009_module_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='progerss',
            field=models.IntegerField(default=0),
        ),
    ]