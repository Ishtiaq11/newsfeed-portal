# Generated by Django 3.1.13 on 2021-10-02 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0016_auto_20211001_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='thumbnail',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
