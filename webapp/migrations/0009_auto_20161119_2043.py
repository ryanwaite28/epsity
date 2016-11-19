# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-19 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20161119_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbio',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_bio_owner', to='webapp.Accounts'),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_info_owner', to='webapp.Accounts'),
        ),
    ]
