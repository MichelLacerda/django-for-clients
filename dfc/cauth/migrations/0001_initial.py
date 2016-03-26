# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cauth.utils


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('profile', models.PositiveSmallIntegerField(default=3, verbose_name='Profile', choices=[(0, 'Administrator'), (1, 'CEO'), (2, 'Agent'), (3, 'Customer')])),
                ('photo', models.ImageField(null=True, upload_to=cauth.utils.directory_path, blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='E-mail')),
                ('first_name', models.CharField(max_length=60, blank=True)),
                ('last_name', models.CharField(max_length=80, blank=True)),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', to='auth.Group', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', to='auth.Permission', verbose_name='', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'permissions': (('can_adm', 'Administrator'), ('can_ceo', 'CEO'), ('can_agent', 'Agent'), ('can_customer', 'Customer')),
            },
        ),
    ]
