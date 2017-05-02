# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 20:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Enrollment', '0012_auto_20161201_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Enrollment.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='enrollmentNo',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]