# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('username', models.CharField(max_length=20, verbose_name='用户名称')),
                ('password', models.CharField(max_length=40, verbose_name='用户密码')),
                ('email', models.EmailField(max_length=254, verbose_name='用户邮箱')),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
    ]
