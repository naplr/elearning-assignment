# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-05 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star', '0002_sessioninfo_quiz_2_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessioninfo',
            name='interactive',
            field=models.BooleanField(default=False),
        ),
    ]
