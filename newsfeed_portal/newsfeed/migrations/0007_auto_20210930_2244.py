# Generated by Django 3.1.13 on 2021-09-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0006_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
