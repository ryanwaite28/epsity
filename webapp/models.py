from __future__ import unicode_literals

from django.db import models
from django.db.models import Model
from django.utils import timezone
import hashlib

# Create your models here.

class Accounts(models.Model):

    ACCOUNT_TYPES = (
        ('Personal', 'Personal'),
        ('Group', 'Group'),
    )

    uname = models.CharField(max_length = 20, default = '')
    displayname = models.CharField(max_length = 20, default = '')
    description = models.CharField(max_length = 100, default = '')
    email = models.CharField(max_length = 50, default = '')
    pswrd = models.CharField(max_length = 50, default = '')
    provider = models.CharField(max_length = 20, default = '')
    provider_id = models.CharField(max_length = 100, default = '')
    avi = models.CharField(max_length = 500, default = '/static/hotspot/img/anon2.png')
    background = models.CharField(max_length = 500, default = '')
    gender = models.CharField(max_length = 25, default = '')
    phone = models.CharField(max_length = 25, default = '')

    type = models.CharField(max_length = 20, choices = ACCOUNT_TYPES, default = '')
    status = models.CharField(max_length = 9, default = 'public') # either public, private or deleted
    official = models.IntegerField() # 1 = True | 0 = False

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "accounts"

# ---

class AccountInfo(models.Model):

    owner = models.ForeignKey(Accounts, related_name = "account_owner", on_delete = models.CASCADE)

    interests = models.CharField(max_length = 1725, default = '')
    seeking = models.CharField(max_length = 1725, default = '')

    class Meta:
        db_table = "accountinfo"

# ---

class Bio(models.Model):

    owner = models.ForeignKey(Accounts, related_name = "bio_owner", on_delete = models.CASCADE)

    bio_desc = models.CharField(max_length = 150, default = '')
    bio_link = models.CharField(max_length = 150, default = '')

    class Meta:
        db_table = "bio"

# ---

class Stats(models.Model):

    owner = models.ForeignKey(Accounts, related_name = "stats_owner", on_delete = models.CASCADE)

    following = models.ForeignKey(Accounts, related_name = "following", on_delete = models.CASCADE)
    followers = models.ForeignKey(Accounts, related_name = "followers", on_delete = models.CASCADE)
    groups = models.ForeignKey(Accounts, related_name = "groups", on_delete = models.CASCADE)
    posts = models.ForeignKey(Accounts, related_name = "posts", on_delete = models.CASCADE)
    likes = models.ForeignKey(Accounts, related_name = "likes", on_delete = models.CASCADE)

    class Meta:
        db_table = "stats"

# ---

class Follows(models.Model):

    user_id = models.IntegerField(blank = False)
    user_rel = models.ForeignKey(Accounts, related_name = "user_rel", on_delete = models.CASCADE)

    follow_id = models.IntegerField(blank = False)
    follow_rel = models.ForeignKey(Accounts, related_name = "follow_rel", on_delete = models.CASCADE)

    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "follows"

# ---

class Posts(models.Model):

    POST_TYPES = (
        ('Text', 'Text'),
        ('Photo', 'Photo'),
        ('Video', 'Video'),
        ('Audio', 'Audio'),
        ('Event', 'Event'),
    )

    owner = models.ForeignKey(Accounts, related_name = "post_owner", on_delete = models.CASCADE)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    image = models.CharField(max_length = 500, default = '')
    link = models.CharField(max_length = 500, default = '')

    type = models.CharField(max_length = 20, choices = POST_TYPES, default = '')
    status = models.CharField(max_length = 20, default = 'public') # either public, private, or deleted

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "posts"

# ---

class Comments(models.Model):

    owner = models.ForeignKey(Accounts, related_name = "comment_owner", on_delete = models.CASCADE, blank = False)

    post_id = models.IntegerField(blank = False)
    post_rel = models.ForeignKey(Posts, on_delete = models.CASCADE, blank = False)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "comments"

# ---

class Likes(models.Model):

    owner = models.ForeignKey(Accounts, related_name = "like_owner", on_delete = models.CASCADE)

    post_id = models.IntegerField(blank = False)
    post_rel = models.ForeignKey(Posts, on_delete = models.CASCADE, blank = False)

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "likes"

# ---

class Conversations(models.Model):

    owner = models.ForeignKey(Accounts, related_name = "convo_owner", on_delete = models.CASCADE)

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "conversations"

# ---

class ConvoMembers(models.Model):

    user = models.ForeignKey(Accounts, related_name = "convo_user", on_delete = models.CASCADE)

    convo_id = models.IntegerField(blank = False)
    convo_rel = models.ForeignKey(Conversations, related_name = "convo_member_rel", on_delete = models.CASCADE)

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "convo_members"

# ---

class ConvoMessages(models.Model):

    user = models.ForeignKey(Accounts, related_name = "convo_user_msg", on_delete = models.CASCADE)

    convo_id = models.IntegerField(blank = False)
    convo_rel = models.ForeignKey(Conversations, related_name = "convo_msg_rel", on_delete = models.CASCADE)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "convo_messages"

# ---
