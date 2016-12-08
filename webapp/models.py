# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

# on_delete = models.CASCADE

from __future__ import unicode_literals

import datetime

from django import forms
from django.db import models
from django.db.models import Model
from django.utils import timezone
import hashlib

from vaults import webapp_dir, pages, localPaths, serverPaths
from vaults import ownerTypes
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# --- --- --- --- --- #
# --- Helper Code --- #
# --- --- --- --- --- #


def returnModelSerialized(type, id):
    if id == None:
        return 'error --- Missing id'

    elif type == '' or type == None:
        return 'error --- invalid type'

    elif type == 'Account':
        obj = Accounts.objects.get(id = id)
        return obj.serialize

    elif type == 'Group':
        obj = Groups.objects.get(id = id)
        return obj.serialize



    else:
        return 'error --- unknown type'


# --- ------ --- #
# --- Models --- #
# --- ------ --- #


class AviModel(models.Model):
    docfile = models.FileField(upload_to='avatars/', default='')

# ---
class WpModel(models.Model):
    docfile = models.FileField(upload_to='backgrounds/', default='')

# ---

class mediaPhotoModel(models.Model):
    docfile = models.FileField(upload_to='media/photo/', default='')

# ---

class mediaVideoModel(models.Model):
    docfile = models.FileField(upload_to='media/video/', default='')

# ---

class mediaAudioModel(models.Model):
    docfile = models.FileField(upload_to='media/audio/', default='')

# ---



class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    docname = models.CharField(max_length = 100, default = '')
# ---

class Accounts(models.Model):

    uname = models.CharField(max_length = 20, default = '')
    displayname = models.CharField(max_length = 30, default = '')
    email = models.CharField(max_length = 50, default = '')
    pswrd = models.CharField(max_length = 50, default = '')
    provider = models.CharField(max_length = 20, default = '')
    provider_id = models.CharField(max_length = 100, default = '')
    avi = models.CharField(max_length = 500, default = '/static/img/anon2.png')
    background = models.CharField(max_length = 500, default = '/static/img/bg-default.jpg')
    gender = models.CharField(max_length = 25, default = '')
    phone = models.CharField(max_length = 25, default = '')

    type = models.CharField(max_length = 20, default = '')
    status = models.CharField(max_length = 9, default = 'public')
    # status: either public, private or deleted

    official = models.IntegerField(default = 0)
    # official: 1 = True | 0 = False

    interests = models.CharField(max_length = 1725, default = '')
    seeking = models.CharField(max_length = 1725, default = '')

    bio_desc = models.CharField(max_length = 150, default = '')
    bio_link = models.CharField(max_length = 150, default = '')
    #bio_link_name = models.CharField(max_length = 100, default = '')

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

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


class Groups(models.Model):

    owner_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_owner")
    ownerid = models.IntegerField(blank = False, default = 0)

    displayname = models.CharField(max_length = 1725, default = '')
    desc = models.CharField(max_length = 1725, default = '')
    uname = models.CharField(max_length = 1725, default = '')
    categories = models.CharField(max_length = 1725, default = '')

    avi = models.CharField(max_length = 1725, default = '')
    background = models.CharField(max_length = 1725, default = '')

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

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
    group_rel = models.ForeignKey(Groups, default = 0, related_name = "i_group_rel")

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "i_group_user")

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'gid': self.id,

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

class GroupRequests(models.Model):

    group_id = models.IntegerField(blank = False, default = 0)
    group_rel = models.ForeignKey(Groups, default = 0, related_name = "r_group_rel")

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "r_group_user")

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'gid': self.id,

            'group_id': self.group_id,
            'group_rel': self.group_rel.serialize,
            'userid': self.userid,
            'user_rel': self.user_rel.serialize,
            'date_created': self.date_created,
            'last_active': self.last_active
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "group_requests"

# ---

class GroupMembers(models.Model):

    group_id = models.IntegerField(blank = False, default = 0)
    group_rel = models.ForeignKey(Groups, default = 0, related_name = "group_member_rel")

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_user_rel")
    status = models.CharField(max_length = 500, default = '') # Admin, user, etc...

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

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


class GroupFavorites(models.Model):

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "fav_user_rel")

    group_id = models.IntegerField(blank = False, default = 0)
    group_rel = models.ForeignKey(Groups, default = 0, related_name = "fav_group_rel")

    date_created = models.DateTimeField( default = datetime.datetime.now )

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'fid': self.id,

            'userid': self.userid,
            'user': self.user_rel.serialize,
            'groupid': self.group_id,
            'group_rel': self.group_rel.serialize,
            'date_created': self.date_created
        }

    class Meta:
        db_table = "favorite_groups"


# --- #
# --- #

class Follows(models.Model):

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "user_rel")

    follow_id = models.IntegerField(blank = False, default = 0)
    follow_rel = models.ForeignKey(Accounts, default = 0, related_name = "follow_rel")

    date_created = models.DateTimeField( default = datetime.datetime.now )

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
    sender_rel = models.ForeignKey(Accounts, default = 0, related_name = "f_sender_rel")

    recipient_id = models.IntegerField(blank = False, default = 0)
    recipient_rel = models.ForeignKey(Accounts, default = 0, related_name = "f_recipient_rel")

    msg = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = datetime.datetime.now )

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

# ------- #
# ------- #


class Posts(models.Model):

    OwnerType = (
        ('Account', 'Account'),
        ('Group', 'Group'),
    )

    PostTypes = (
        ('Text', 'Text'),
        ('Photo', 'Photo'),
        ('Audio', 'Audio'),
        ('Video', 'Video'),
    )

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    title = models.CharField(max_length = 500, default = '')
    contents = models.CharField(max_length = 500, default = '')
    link = models.CharField(max_length = 500, default = '')

    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    post_type = models.CharField(max_length = 20, choices = PostTypes, default = '')
    status = models.CharField(max_length = 20, default = 'public') # either public, private, or deleted

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'p_id': self.id,

            'ownerid': self.ownerid,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'title': self.title,
            'contents': self.contents,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'link': self.link,
            'post_type': self.post_type,
            'status': self.status,
            'date_created': self.date_created,
            'last_active': self.last_active
        }

    class Meta:
        db_table = "posts"

# ---

class Comments(models.Model):

    OwnerType = (
        ('Account', 'Account'),
        ('Group', 'Group'),
    )

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    post_id = models.IntegerField(blank = False, default = 0)
    post_rel = models.ForeignKey(Posts, default = 0, on_delete = models.CASCADE, blank = False)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'comment_id': self.id,

            'ownerid': self.ownerid,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'post_id': self.post_id,
            'post_rel': self.post_rel.serialize,
            'contents': self.contents,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'date_created': self.date_created,
            'last_active': self.last_active
        }

    class Meta:
        db_table = "comments"

# ---

class Replies(models.Model):

    OwnerType = (
        ('Account', 'Account'),
        ('Group', 'Group'),
    )

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    comment_id = models.IntegerField(blank = False, default = 0)
    comment_rel = models.ForeignKey(Comments, default = 0, on_delete = models.CASCADE, blank = False)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'reply_id': self.id,

            'ownerid': self.ownerid,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'comment_id': self.comment_id,
            'comment_rel': self.comment_rel.serialize,
            'contents': self.contents,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'date_created': self.date_created,
            'last_active': self.last_active
        }

    class Meta:
        db_table = "replies"

# ---

class Likes(models.Model):

    OwnerType = (
        ('Account', 'Account'),
        ('Group', 'Group'),
    )

    ContentType = (
        ('Post', 'Post'),
        ('Comment', 'Comment'),
        ('Reply', 'Reply'),
        ('Group', 'Group'),
        ('Event', 'Event'),
    )

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    item_type = models.CharField(choices = ContentType, blank = False, default = '', max_length = 50)
    item_id = models.IntegerField(blank = False, default = 0)

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'like_id': self.id,

            'ownerid': self.ownerid,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'item_type': self.item_type.serialize,
            'item_id': self.item_id,
            'date_created': self.date_created,
            'last_active': self.last_active
        }

    class Meta:
        db_table = "likes"

# ---

class Events(models.Model):

    OwnerType = (
        ('Account', 'Account'),
        ('Group', 'Group'),
    )

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    title = models.CharField(max_length = 500, default = '')
    desc = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')
    link = models.CharField(max_length = 500, default = '')

    categories = models.CharField(max_length = 500, default = '')

    start_datetime = models.DateTimeField(blank = False, default = 0)
    end_datetime = models.DateTimeField(blank = False, default = 0)

    status = models.CharField(max_length = 20, default = 'upcoming')
    # either upcoming, live, or ended

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'eid': self.id,

            'ownerid': self.ownerid,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'tilte': self.title,
            'desc': self.desc,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'link': self.link,
            'categories': self.categories,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'status': self.status,
            'date_created': self.date_created,
            'last_active': self.last_active
        }

    class Meta:
        db_table = "events"

# ---


class EventAttendees(models.Model):

    OwnerType = (
        ('Account', 'Account'),
        ('Group', 'Group'),
    )

    event_id = models.IntegerField(blank = False, default = 0)
    event_rel = models.ForeignKey(Events, default = 0, related_name = "event_rel")

    attendee_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)
    attendee_id = models.IntegerField(blank = False, default = 0)

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'aid': self.id,

            'evenr_rel': self.event_rel.serialize,
            'event_id': self.event_id,
            'attendee': returnModelSerialized( self.attendee_type, self.attendee_id ),
            'attendee_id': self.attendee_id,
            'attendee_type': self.attendee_type,
            'date_created': self.date_created,
            'last_active': self.last_active
        }

    class Meta:
        db_table = "event_attendees"


# ------- #
# ------- #

class Conversations(models.Model):

    owner = models.ForeignKey(Accounts, default = 0, related_name = "convo_owner")
    ownerid = models.IntegerField(blank = False, default = 0)

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

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

    user = models.ForeignKey(Accounts, default = 0, related_name = "convo_user")
    userid = models.IntegerField(blank = False, default = 0)

    convo_id = models.IntegerField(blank = False, default = 0)
    convo_rel = models.ForeignKey(Conversations, default = 0, related_name = "convo_member_rel")

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'cvm_id': self.id,
            'user': self.user.serialize,
            'userid': self.userid,
            'convo_id': self.convo_id,
            'convo_rel': self.convo_rel.serialize

        }

    class Meta:
        db_table = "convo_members"

# ---

class ConvoMessages(models.Model):

    user = models.ForeignKey(Accounts, default = 0, related_name = "convo_user_msg")
    userid = models.IntegerField(blank = False, default = 0)

    convo_id = models.IntegerField(blank = False, default = 0)
    convo_rel = models.ForeignKey(Conversations, default = 0, related_name = "convo_msg_rel")

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'cvm_id': self.id,
            'user': self.user.serialize,
            'userid': self.userid,
            'convo_id': self.convo_id,
            'convo_rel': self.convo_rel.serialize,
            'contents': self.contents,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'date_created': self.date_created,
        }

    class Meta:
        db_table = "convo_messages"

# ---

class Notifications(models.Model):

    type = models.CharField(max_length = 1725, default = '')

    sender_id = models.IntegerField(blank = False, default = 0)
    sender_rel = models.ForeignKey(Accounts, default = 0, related_name = "notif_sender_owner")

    recipient_id = models.IntegerField(blank = False, default = 0)
    recipient_rel = models.ForeignKey(Accounts, default = 0, related_name = "notif_recipient_owner")

    text = models.CharField(max_length = 1725, default = '')
    link = models.CharField(max_length = 1725, default = '')
    date_created = models.DateTimeField(auto_now=True)

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

class Messages(models.Model):

    userA_id = models.IntegerField(blank = False, default = 0)
    userA_rel = models.ForeignKey(Accounts, default = 0, related_name = "message_user_a_rel")

    userB_id = models.IntegerField(blank = False, default = 0)
    userB_rel = models.ForeignKey(Accounts, default = 0, related_name = "message_user_b_rel")

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'mid': self.id,

            'userA_id': self.userA_id,
            'userA_rel': self.userA_rel.serialize,
            'userB_id': self.userB_id,
            'userB_rel': self.userB_rel.serialize,
            'date_created': self.date_created,
            'last_active': self.last_active
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "messages"


# ---

class MessageReply(models.Model):

    message_id = models.IntegerField(blank = False, default = 0)
    message_rel = models.ForeignKey(Messages, default = 0, related_name = "messagereply_user_rel")

    userid = models.IntegerField(blank = False, default = 0)
    user_rel = models.ForeignKey(Accounts, default = 0, related_name = "messagereply_user_rel")

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = datetime.datetime.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'mr_id': self.id,

            'message_id': self.message_id,
            #'message_rel': self.message_rel.serialize,
            'userid': self.userid,
            'user_rel': self.user_rel.serialize,
            'contents': self.contents,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'date_created': self.date_created,
            'last_active': self.last_active
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "messagereplies"
