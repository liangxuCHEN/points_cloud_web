# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 04:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('three_d', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DxfModel',
            new_name='TDModel',
        ),
    ]
