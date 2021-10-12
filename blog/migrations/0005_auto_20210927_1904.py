# Generated by Django 3.2.7 on 2021-09-27 19:04

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180131_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='正文'),
        ),
    ]