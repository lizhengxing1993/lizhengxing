# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_delete_booksmanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/root/bookstore/bookstore/collect_static'), upload_to='books', verbose_name='商品图片'),
        ),
    ]
