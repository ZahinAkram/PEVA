# Generated by Django 2.0.7 on 2018-08-29 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PEVA', '0014_auto_20180829_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='shared_event',
            name='complete2',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 29, 18, 34, 28, 616302)),
        ),
    ]
