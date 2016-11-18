# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-18 03:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interests', models.CharField(default='', max_length=1725)),
                ('seeking', models.CharField(default='', max_length=1725)),
            ],
            options={
                'db_table': 'accountinfo',
            },
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(default='', max_length=20)),
                ('displayname', models.CharField(default='', max_length=20)),
                ('description', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=50)),
                ('pswrd', models.CharField(default='', max_length=50)),
                ('provider', models.CharField(default='', max_length=20)),
                ('provider_id', models.CharField(default='', max_length=100)),
                ('avi', models.CharField(default='/static/hotspot/img/anon2.png', max_length=500)),
                ('background', models.CharField(default='/static/hotspot/img/bg-1.jpg', max_length=500)),
                ('gender', models.CharField(default='', max_length=25)),
                ('phone', models.CharField(default='', max_length=25)),
                ('type', models.CharField(choices=[('Personal', 'Personal'), ('Group', 'Group')], default='', max_length=20)),
                ('status', models.CharField(default='public', max_length=9)),
                ('official', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_active', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Bio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio_desc', models.CharField(default='', max_length=150)),
                ('bio_link', models.CharField(default='', max_length=150)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bio_owner', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'bio',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('contents', models.CharField(default='', max_length=500)),
                ('attachment', models.CharField(default='', max_length=500)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_active', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_owner', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Conversations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_active', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convo_owner', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'conversations',
            },
        ),
        migrations.CreateModel(
            name='ConvoMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('convo_id', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_active', models.DateField(auto_now=True)),
                ('convo_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convo_member_rel', to='webapp.Conversations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convo_user', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'convo_members',
            },
        ),
        migrations.CreateModel(
            name='ConvoMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('convo_id', models.IntegerField()),
                ('contents', models.CharField(default='', max_length=500)),
                ('attachment', models.CharField(default='', max_length=500)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_active', models.DateField(auto_now=True)),
                ('convo_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convo_msg_rel', to='webapp.Conversations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convo_user_msg', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'convo_messages',
            },
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('follow_id', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('follow_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_rel', to='webapp.Accounts')),
                ('user_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rel', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'follows',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_active', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_owner', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'likes',
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=1725)),
                ('n_type', models.CharField(default='', max_length=1725)),
                ('sender_id', models.IntegerField()),
                ('recipient_id', models.IntegerField()),
                ('text', models.CharField(default='', max_length=1725)),
                ('date_created', models.DateField(auto_now=True)),
                ('link', models.CharField(default='', max_length=1725)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_owner', to='webapp.Accounts')),
                ('recipient_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_recipient_owner', to='webapp.Accounts')),
                ('sender_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_sender_owner', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'notifications',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.CharField(default='', max_length=500)),
                ('attachment', models.CharField(default='', max_length=500)),
                ('image', models.CharField(default='', max_length=500)),
                ('link', models.CharField(default='', max_length=500)),
                ('type', models.CharField(choices=[('Text', 'Text'), ('Photo', 'Photo'), ('Video', 'Video'), ('Audio', 'Audio'), ('Event', 'Event')], default='', max_length=20)),
                ('status', models.CharField(default='public', max_length=20)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('last_active', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_owner', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'posts',
            },
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='webapp.Accounts')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='webapp.Accounts')),
                ('groups', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='webapp.Accounts')),
                ('likes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='webapp.Accounts')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats_owner', to='webapp.Accounts')),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='webapp.Accounts')),
            ],
            options={
                'db_table': 'stats',
            },
        ),
        migrations.AddField(
            model_name='likes',
            name='post_rel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Posts'),
        ),
        migrations.AddField(
            model_name='comments',
            name='post_rel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Posts'),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_owner', to='webapp.Accounts'),
        ),
    ]
