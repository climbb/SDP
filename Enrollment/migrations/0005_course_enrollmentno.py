# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enrollment', '0004_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='enrollmentNo',
            field=models.IntegerField(default=0),
        ),
    ]
