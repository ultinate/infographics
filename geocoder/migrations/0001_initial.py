# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-26 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeocodeCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True)),
                ('key', models.CharField(max_length=500)),
                ('hash', models.CharField(max_length=100)),
                ('is_zero_results', models.BooleanField(help_text='Indicates whether google has returned ZERO_RESULTSfor this address.')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('accessed', models.DateTimeField()),
            ],
        ),
    ]
