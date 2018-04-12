# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='recioient_addr',
            new_name='recipient_addr',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='recioient_name',
            new_name='recipient_name',
        ),
    ]
