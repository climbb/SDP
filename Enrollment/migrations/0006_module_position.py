# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-25 18:27
from __future__ import unicode_literals

from django.db import migrations
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Enrollment', '0005_course_enrollmentno'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='position',
            field=positions.fields.PositionField(default=-1),
        ),
    ]
