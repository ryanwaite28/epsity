# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-19 21:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_auto_20161119_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountbio',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='accountinfo',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='post_rel',
        ),
        migrations.RemoveField(
            model_name='conversations',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='convomembers',
            name='convo_rel',
        ),
        migrations.RemoveField(
            model_name='convomembers',
            name='user',
        ),
        migrations.RemoveField(
            model_name='convomessages',
            name='convo_rel',
        ),
        migrations.RemoveField(
            model_name='convomessages',
            name='user',
        ),
        migrations.RemoveField(
            model_name='follows',
            name='follow_rel',
        ),
        migrations.RemoveField(
            model_name='follows',
            name='user_rel',
        ),
        migrations.RemoveField(
            model_name='groupmembers',
            name='group_rel',
        ),
        migrations.RemoveField(
            model_name='groupmembers',
            name='user_rel',
        ),
        migrations.RemoveField(
            model_name='groups',
            name='owner_rel',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='post_rel',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='recipient_rel',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='sender_rel',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='owner',
        ),
    ]
