# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20160508_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='current_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True),
        ),
    ]
