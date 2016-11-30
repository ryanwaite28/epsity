from __future__ import unicode_literals

from django import forms
from django.db import models
from django.db.models import Model
from django.utils import timezone
import hashlib

from vaults import webapp_dir, pages, errorPage, localPaths, serverPaths

# ---

class AviModel(models.Model):
    docfile = models.FileField(upload_to='avatars/', default='')

# ---
class WpModel(models.Model):
    docfile = models.FileField(upload_to='backgrounds/', default='')

# ---

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    docname = models.CharField(max_length = 100, default = '')
# ---

class Accounts(models.Model):

    ACCOUNT_TYPES = (
        ('Personal', 'Personal'),
        ('Group', 'Group'),
    )

    uname = models.CharField(max_length = 20, default = '')
    displayname = models.CharField(max_length = 30, default = '')
    email = models.CharField(max_length = 50, default = '')
    pswrd = models.CharField(max_length = 50, default = '')
    provider = models.CharField(max_length = 20, default = '')
    provider_id = models.CharField(max_length = 100, default = '')
    avi = models.CharField(max_length = 500, default = '/static/hotspot/img/anon2.png')
    # avi = models.ImageField(upload_to=localPaths['avatars_rel'], max_length = 500, default = '/static/hotspot/img/anon2.png')
    background = models.CharField(max_length = 500, default = '')
    # background = models.ImageField(upload_to=localPaths['backgrounds_rel'], max_length = 500, default = '/static/img/grafitti-1.jpg')
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
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'userid': self.id,
            'uname': self.uname,
            'displayname': self.displayname,
            'avi': self.avi,
            'status': self.status,
            'background': self.background,
        }

    @property
    def get_bio(self):
         # Returns Data Object In Proper Format
        return {
            'desc': self.bio_desc,
            'link': self.bio_link,
            #'linkName': self.bio_link_name,
        }

    @property
    def get_info(self):
         # Returns Data Object In Proper Format
        return {
            'interests': self.interests,
            'seeking': self.seeking,
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

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'fid': self.id,

            'userid': self.userid,
            'user': self.user_rel.serialize,
            'followid': self.follow_id,
            'follow': self.follow_rel.serialize,
            'date_created': self.date_created
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "follows"

# ---

class FollowRequests(models.Model):

    sender_id = models.IntegerField(blank = False, default = 0)
    sender_rel = models.ForeignKey(Accounts, default = 0, related_name = "f_sender_rel", on_delete = models.CASCADE)

    recipient_id = models.IntegerField(blank = False, default = 0)
    recipient_rel = models.ForeignKey(Accounts, default = 0, related_name = "f_recipient_rel", on_delete = models.CASCADE)

    msg = models.CharField(max_length = 500, default = '')

    date_created = models.DateField(auto_now_add=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'fid': self.id,

            'senderid': self.sender_id,
            'sender_rel': self.sender_rel.serialize,
            'recipientid': self.recipient_id,
            'recipient_rel': self.recipient_rel.serialize,
            'msg': self.msg,
            'date_created': self.date_created
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "follow_requests"

# ---

class Posts(models.Model):

    POST_TYPES = (
        ('Text', 'Text'),
        ('Photo', 'Photo'),
        ('Video', 'Video'),
        ('Audio', 'Audio'),
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

    @property
    def serialize(self):
        return {
            'owner': self.owner.serialize,
            'ownerid': self.ownerid,
            'date_created': self.date_created,
            'last_active': self.last_active
        }

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

    sender_id = models.IntegerField(blank = False, default = 0)
    sender_rel = models.ForeignKey(Accounts, default = 0, related_name = "notif_sender_owner", on_delete = models.CASCADE)

    recipient_id = models.IntegerField(blank = False, default = 0)
    recipient_rel = models.ForeignKey(Accounts, default = 0, related_name = "notif_recipient_owner", on_delete = models.CASCADE)

    text = models.CharField(max_length = 1725, default = '')
    link = models.CharField(max_length = 1725, default = '')
    date_created = models.DateField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'notif_id': self.id,
            'type': self.type,
            'senderid': self.sender_id,
            'sender_rel': self.sender_rel.serialize,
            'recipientid': self.recipient_id,
            'recipient_rel': self.recipient_rel.serialize,
            'text': self.text,
            'link': self.link,
            'date_created': self.date_created
        }

    class Meta:
        db_table = "notifications"

# ---

class Groups(models.Model):

    owner_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_owner") # on_delete = models.CASCADE
    ownerid = models.IntegerField(blank = False, default = 0)

    displayname = models.CharField(max_length = 1725, default = '')
    desc = models.CharField(max_length = 1725, default = '')
    uname = models.CharField(max_length = 1725, default = '')
    categories = models.CharField(max_length = 1725, default = '')

    avi = models.CharField(max_length = 1725, default = '')
    background = models.CharField(max_length = 1725, default = '')

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'gid': self.id,
            'displayname': self.displayname,
            'uname': self.uname,
            'desc': self.desc,
            'avi': self.avi,
            'background': self.background,
            'categories': self.categories.split(';'),
            'owner': self.owner_rel.serialize
        }

    class Meta:
        db_table = "groups"

# ---

class GroupInvitations(models.Model):

    group_id = models.IntegerField(blank = False, default = 0)
    group_rel = models.ForeignKey(Groups, default = 0, related_name = "group_rel", on_delete = models.CASCADE)

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_user", on_delete = models.CASCADE)

    # status = models.CharField(max_length = 1725, default = '')

    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'gmid': self.id,

            'group_id': self.group_id,
            'group_rel': self.group_rel.serialize,
            'userid': self.userid,
            'user_rel': self.user_rel.serialize,
            'date_created': self.date_created,
            'last_active': self.last_active
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "group_invitations"

# ---

class GroupMembers(models.Model):

    group_id = models.IntegerField(blank = False, default = 0)
    group_rel = models.ForeignKey(Groups, default = 0, related_name = "group_member_rel", on_delete = models.CASCADE)

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_user_rel", on_delete = models.CASCADE)


    date_created = models.DateField(auto_now_add=True)
    last_active = models.DateField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'gmid': self.id,

            'group_id': self.group_id,
            'group_rel': self.group_rel.serialize,
            'userid': self.userid,
            'user_rel': self.user_rel.serialize,
            'date_created': self.date_created,
            'last_active': self.last_active
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "group_members"

# ---
