# Generated by Django 3.2.7 on 2021-10-11 14:41

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210927_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='正文'),
        ),
    ]
