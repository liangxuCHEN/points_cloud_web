# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 04:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DxfModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='模型名字')),
                ('uploads', models.FileField(upload_to='dxf_files/', verbose_name='上传文件')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
