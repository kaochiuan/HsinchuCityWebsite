# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151128_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnamialHospitalReputation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('hospitalName', models.CharField(max_length=300)),
                ('address', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('postiveScore', models.IntegerField()),
                ('negativeScore', models.IntegerField()),
                ('dataDT', models.DateField()),
            ],
        ),
    ]
