# Generated by Django 4.1.2 on 2022-10-17 14:18

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_service_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('services', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
    ]
