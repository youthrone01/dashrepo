# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 19:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver',
        ),
    ]