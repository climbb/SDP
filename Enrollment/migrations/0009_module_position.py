# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 17:46
from __future__ import unicode_literals

from django.db import migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Enrollment', '0008_auto_20161125_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='position',
            field=positions.fields.PositionField(default=0),
        ),
    ]
