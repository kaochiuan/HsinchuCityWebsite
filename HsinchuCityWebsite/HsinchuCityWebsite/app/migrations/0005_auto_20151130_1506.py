# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_anamialhospitalreputation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anamialhospitalreputation',
            old_name='hospitalName',
            new_name='name',
        ),
    ]
