# Generated by Django 2.0.7 on 2018-08-01 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250)),
                ('Date_of_Birth', models.CharField(max_length=250)),
                ('Address', models.CharField(max_length=500)),
                ('Email_Address', models.CharField(max_length=250)),
                ('Gender', models.CharField(max_length=25)),
            ],
        ),
    ]
