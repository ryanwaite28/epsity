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
    email = models.CharField(max_length = 50, default = '')
    pswrd = models.CharField(max_length = 50, default = '')
    provider = models.CharField(max_length = 20, default = '')
    provider_id = models.CharField(max_length = 100, default = '')
    avi = models.CharField(max_length = 500, default = '/static/hotspot/img/anon2.png')
    background = models.CharField(max_length = 500, default = '/static/hotspot/img/bg-1.jpg')
    gender = models.CharField(max_length = 25, default = '')
    phone = models.CharField(max_length = 25, default = '')

    type = models.CharField(max_length = 20, choices = ACCOUNT_TYPES, default = '')
    status = models.CharField(max_length = 9, default = 'public') # either public, private or deleted
    official = models.IntegerField(default = 0) # 1 = True | 0 = False

    interests = models.CharField(max_length = 1725, default = '')
    seeking = models.CharField(max_length = 1725, default = '')

    bio_desc = models.CharField(max_length = 150, default = '')
    bio_link = models.CharField(max_length = 150, default = '')
    #bio_link_name = models.CharField(max_length = 100, default = '')

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    @property
    def serialize_basic(self):
         # Returns Data Object In Proper Format
        return {
            'userid': self.id,
            'uname': self.uname,
            'avi': self.avi
        }

    @property
    def get_bio(self):
         # Returns Data Object In Proper Format
        return {
            'desc': self.bio_desc,
            'link': self.bio_link,
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "accounts"

# --- #
# --- #
# --- #

class Follows(models.Model):

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "user_rel", on_delete = models.CASCADE)

    follow_id = models.IntegerField(blank = False, default = 0)
    follow_rel = models.ForeignKey(Accounts, default = 0, related_name = "follow_rel", on_delete = models.CASCADE)

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

    owner = models.ForeignKey(Accounts, default = 0, related_name = "post_owner", on_delete = models.CASCADE)
    ownerid = models.IntegerField(blank = False, default = 0)

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

    owner = models.ForeignKey(Accounts, default = 0, related_name = "comment_owner", on_delete = models.CASCADE, blank = False)
    ownerid = models.IntegerField(blank = False, default = 0)

    post_id = models.IntegerField(blank = False, default = 0)
    post_rel = models.ForeignKey(Posts, default = 0, on_delete = models.CASCADE, blank = False)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "comments"

# ---

class Likes(models.Model):

    owner = models.ForeignKey(Accounts, default = 0, related_name = "like_owner", on_delete = models.CASCADE)
    ownerid = models.IntegerField(blank = False, default = 0)

    post_id = models.IntegerField(blank = False, default = 0)
    post_rel = models.ForeignKey(Posts, default = 0, on_delete = models.CASCADE, blank = False)

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "likes"

# ---

class Conversations(models.Model):

    owner = models.ForeignKey(Accounts, default = 0, related_name = "convo_owner", on_delete = models.CASCADE)
    ownerid = models.IntegerField(blank = False, default = 0)

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "conversations"

# ---

class ConvoMembers(models.Model):

    user = models.ForeignKey(Accounts, default = 0, related_name = "convo_user", on_delete = models.CASCADE)
    userid = models.IntegerField(blank = False, default = 0)

    convo_id = models.IntegerField(blank = False, default = 0)
    convo_rel = models.ForeignKey(Conversations, default = 0, related_name = "convo_member_rel", on_delete = models.CASCADE)

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "convo_members"

# ---

class ConvoMessages(models.Model):

    user = models.ForeignKey(Accounts, default = 0, related_name = "convo_user_msg", on_delete = models.CASCADE)
    userid = models.IntegerField(blank = False, default = 0)

    convo_id = models.IntegerField(blank = False, default = 0)
    convo_rel = models.ForeignKey(Conversations, default = 0, related_name = "convo_msg_rel", on_delete = models.CASCADE)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "convo_messages"

# ---

class Notifications(models.Model):

    type = models.CharField(max_length = 1725, default = '')
    n_type = models.CharField(max_length = 1725, default = '')

    sender_id = models.IntegerField(blank = False, default = 0)
    sender_rel = models.ForeignKey(Accounts, default = 0, related_name = "notif_sender_owner", on_delete = models.CASCADE)

    recipient_id = models.IntegerField(blank = False, default = 0)
    recipient_rel = models.ForeignKey(Accounts, default = 0, related_name = "notif_recipient_owner", on_delete = models.CASCADE)

    text = models.CharField(max_length = 1725, default = '')
    date_created = models.DateField(auto_now=True)
    link = models.CharField(max_length = 1725, default = '')

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'notif_id': self.id
        }

    class Meta:
        db_table = "notifications"

# ---

class Groups(models.Model):

    owner_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_owner", on_delete = models.CASCADE)
    ownerid = models.IntegerField(blank = False, default = 0)

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "groups"

# ---

class GroupMembers(models.Model):

    group_id = models.IntegerField(blank = False, default = 0)
    group_rel = models.ForeignKey(Groups, default = 0, related_name = "group_member_rel", on_delete = models.CASCADE)

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_user", on_delete = models.CASCADE)


    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    class Meta:
        db_table = "group_members"

# ---
