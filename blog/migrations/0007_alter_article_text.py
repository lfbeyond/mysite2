# Generated by Django 3.2.7 on 2021-10-11 18:22

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_article_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=mdeditor.fields.MDTextField(verbose_name='正文'),
        ),
    ]