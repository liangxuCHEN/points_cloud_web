# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 08:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('three_d', '0004_auto_20170925_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objmodel',
            name='upload_mtl',
            field=models.FileField(null=True, upload_to='model/obj', verbose_name='上传mtl文件'),
        ),
    ]