# Generated by Django 2.0.7 on 2018-08-30 07:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PEVA', '0015_auto_20180829_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shared_event',
            options={'ordering': []},
        ),
        migrations.AlterField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 30, 13, 7, 46, 679152)),
        ),
    ]
