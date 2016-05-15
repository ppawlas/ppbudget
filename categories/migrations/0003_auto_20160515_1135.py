# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='level',
        ),
        migrations.AddField(
            model_name='category',
            name='root_node',
            field=models.BooleanField(default=False),
        ),
    ]
