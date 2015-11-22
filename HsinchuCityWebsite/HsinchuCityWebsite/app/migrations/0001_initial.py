# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TempleInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('locateRegion', models.CharField(max_length=10)),
                ('religiousBelief', models.CharField(max_length=50)),
                ('masterGod', models.CharField(max_length=50)),
                ('address', models.TextField(blank=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('phone1', models.CharField(max_length=20, blank=True)),
                ('phone2', models.CharField(max_length=20, blank=True)),
            ],
        ),
    ]
