# Generated by Django 2.2.10 on 2020-05-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_auto_20200507_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='release_date_time',
        ),
        migrations.AddField(
            model_name='projects',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
