# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=31)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('founded_date', models.DateField()),
                ('contact', models.EmailField(max_length=254)),
                ('website', models.URLField()),
            ],
            options={
                'ordering': ['name'],
                'get_latest_by': 'founded_date',
                'verbose_name_plural': 'charities',
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('charity', models.ForeignKey(to='giving.Charity')),
                ('donor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=31)),
                ('last_name', models.CharField(max_length=61)),
                ('last_login', models.DateField()),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
                'get_latest_by': 'last_login',
            },
        ),
    ]
