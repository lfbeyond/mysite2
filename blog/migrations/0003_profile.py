# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-06 14:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20170926_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='static/image/default.jpg', max_length=200, null=True, upload_to='static/image/%Y/%m', verbose_name='用户头像')),
                ('created_dt', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
