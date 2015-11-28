# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityNewsItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=300)),
                ('type', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('publishDate', models.DateField()),
                ('endDate', models.DateField()),
                ('picturePath', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='CultureActiviyInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('activityTheme', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('activityTime', models.CharField(max_length=50)),
                ('locationName', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
    ]
