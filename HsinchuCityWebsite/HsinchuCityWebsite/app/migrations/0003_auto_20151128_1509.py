# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_citynewsitem_cultureactiviyinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cultureactiviyinfo',
            name='endDate',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cultureactiviyinfo',
            name='startDate',
            field=models.CharField(max_length=50),
        ),
    ]
