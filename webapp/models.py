# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

# on_delete = models.CASCADE

from __future__ import unicode_literals

import datetime
from datetime import datetime, timedelta

import random, string, os, paramiko
from django import forms
from django.db import models
from django.db.models import Model
from django.utils import timezone
import hashlib

import vaults
from vaults import masterDICT
from vaults import webapp_dir, pages, localPaths, serverPaths
from vaults import ownerTypes

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# --- --- --- --- --- #
# --- Helper Code --- #
# --- --- --- --- --- #

def randomUniqueValue():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(33))

    return state


def returnModelSerialized(type, id):
    if id == None:
        return None

    elif type == '' or type == None:
        return None



    elif type == 'Account':
        obj = Accounts.objects.get(id = id)
        return obj.serialize

    elif type == 'Group':
        obj = Groups.objects.get(id = id)
        return obj.serialize

    elif type == 'Product':
        obj = Products.objects.get(id = id)
        return obj.serialize

    elif type == 'Service':
        obj = Services.objects.get(id = id)
        return obj.serialize

    elif type == 'Event':
        obj = Events.objects.get(id = id)
        return obj.serialize



    else:
        return None


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
    pswrd_hash = models.CharField(max_length = 250, blank = False, default = '')
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
    bio_link_name = models.CharField(max_length = 100, default = '')

    paypal_email = models.CharField(max_length = 1725, default = '')
    # should be verified

    unique_val = models.CharField(max_length = 125, default = randomUniqueValue )

    date_created = models.DateTimeField( default = timezone.now )
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
            'unique_val': self.unique_val,
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


class Featured(models.Model):
    '''
    For Features
    ------------

    There Can Only Be A Max Of:
    - 10 Features Per Day
    - 10 Features Per Week
    - 10 Features Per Month

    '''

    OwnerType = vaults.OwnerType
    ItemType = vaults.ItemType
    FeaturedStatus = vaults.FeaturedStatus
    FeaturedType = vaults.FeaturedType

    # ---

    unique_val = models.CharField(max_length = 125, default = randomUniqueValue )

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    item_id = models.IntegerField(blank = False, default = 0)
    item_type = models.CharField(choices = ItemType, blank = False, default = '', max_length = 50)

    duration = models.IntegerField(blank = False, default = 0)
    # Number Of Days

    date_started = models.DateTimeField( default = timezone.now )
    date_end = models.DateTimeField( )

    status = models.CharField(choices = FeaturedStatus, blank = False, default = '', max_length = 50)
    type = models.CharField(choices = FeaturedType, blank = False, default = '', max_length = 50)
    # Either Live Expired

    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {

        }

    class Meta:
        db_table = "featured"

# ---


class Groups(models.Model):

    owner_rel = models.ForeignKey(Accounts, default = 0, related_name = "group_owner")
    ownerid = models.IntegerField(blank = False, default = 0)

    displayname = models.CharField(max_length = 1725, default = '')
    desc = models.CharField(max_length = 1725, default = '')
    uname = models.CharField(max_length = 1725, default = '')
    categories = models.CharField(max_length = 1725, default = '')

    avi = models.CharField(max_length = 1725, default = '')
    background = models.CharField(max_length = 1725, default = '')

    date_created = models.DateTimeField( default = timezone.now )
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

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
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

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
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

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
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

    date_created = models.DateTimeField( default = timezone.now )

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'fid': self.id,

            'userid': self.userid,
            'user': self.user_rel.serialize,
            'groupid': self.group_id,
            'group_rel': self.group_rel.serialize,
            'date_created': str(self.date_created)
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

    date_created = models.DateTimeField( default = timezone.now )

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'fid': self.id,

            'userid': self.userid,
            'user': self.user_rel.serialize,
            'followid': self.follow_id,
            'follow': self.follow_rel.serialize,
            'date_created': str(self.date_created)
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

    date_created = models.DateTimeField( default = timezone.now )

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
            'date_created': str(self.date_created)
            #'linkName': self.bio_link_name,
        }

    class Meta:
        db_table = "follow_requests"

# ------- #
# ------- #

class ShareContent(models.Model):
    OwnerType = vaults.OwnerType
    ItemType = vaults.ItemType

    # --- #

    item_id = models.IntegerField(blank = False, default = 0)
    item_type = models.CharField(choices = ItemType, blank = False, default = '', max_length = 50)

    from_id = models.IntegerField(blank = False, default = 0)
    from_rel = models.ForeignKey(Accounts, default = 0, on_delete = models.CASCADE, blank = False)

    ownerid = models.IntegerField(blank = False, default = 0) # related_name = "share_owner"
    owner_rel = models.ForeignKey(Accounts, default = 0, on_delete = models.CASCADE, blank = False, related_name = "share_owner")

    date_created = models.DateTimeField( default = timezone.now )

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_type': self.item_type,
            'from_id': self.from_id,
            'from_rel': self.from_rel.serialize,
            'ownerid': self.ownerid,
            'owner_rel': self.owner_rel.serialize,
        }

    class Meta:
        db_table = "sharecontent"

# --- #
# --- #

class Posts(models.Model):
    OwnerType = vaults.OwnerType
    PostTypes = vaults.PostTypes
    PostStatuses = vaults.PostStatuses

    # ---

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    wall_id = models.IntegerField(blank = False, default = 0)
    wall_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    title = models.CharField(max_length = 500, default = '')
    contents = models.CharField(max_length = 500, default = '')
    link = models.CharField(max_length = 500, default = '')

    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    post_type = models.CharField(max_length = 20, choices = PostTypes, default = '')
    status = models.CharField(max_length = 20, choices = PostStatuses, default = 'public')
    # either public, private, personal, or deleted

    date_created = models.DateTimeField( default = timezone.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'p_id': self.id,

            'ownerid': self.ownerid,
            'owner_type': self.owner_type,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'wall_id': self.wall_id,
            'wall_type': self.wall_type,
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

    @property
    def likes_len(self):
        return len(Likes.objects.filter(item_id = self.id, item_type = 'Post'))

    @property
    def comments_len(self):
        return len(Comments.objects.filter(post_id = self.id))

    @property
    def comments(self):
        return [c.serialize for c in Comments.objects.filter(post_id = self.id)]

    class Meta:
        db_table = "posts"

# ---

class Comments(models.Model):
    OwnerType = vaults.OwnerType

    # ---

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    post_id = models.IntegerField(blank = False, default = 0)
    post_rel = models.ForeignKey(Posts, default = 0, on_delete = models.CASCADE, blank = False)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    @property
    def likes_len(self):
        return len(Likes.objects.filter(item_id = self.id, item_type = 'Comment'))

    @property
    def replies_len(self):
        return len(Replies.objects.filter(comment_id = self.id))

    @property
    def replies(self):
        return [r.serialize for r in Replies.objects.filter(comment_id = self.id)]

    class Meta:
        db_table = "comments"

# ---

class Replies(models.Model):
    OwnerType = vaults.OwnerType

    # ---

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    comment_id = models.IntegerField(blank = False, default = 0)
    comment_rel = models.ForeignKey(Comments, default = 0, on_delete = models.CASCADE, blank = False)

    contents = models.CharField(max_length = 500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    @property
    def likes_len(self):
        return len(Likes.objects.filter(item_id = self.id, item_type = 'Reply'))

    class Meta:
        db_table = "replies"

# ---

class Likes(models.Model):
    OwnerType = vaults.OwnerType
    ContentType = vaults.ContentType

    # ---

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    item_type = models.CharField(choices = ContentType, blank = False, default = '', max_length = 50)
    item_id = models.IntegerField(blank = False, default = 0)

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    class Meta:
        db_table = "likes"

# ---

class Events(models.Model):
    OwnerType = vaults.OwnerType
    AttachmentTypes = vaults.AttachmentTypes

    # ---

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    name = models.CharField(max_length = 500, default = '')
    desc = models.CharField(max_length = 500, default = '')
    place = models.CharField(max_length = 500, default = '')
    location = models.CharField(max_length = 500, default = '')
    link = models.CharField(max_length = 500, default = '')

    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(choices = AttachmentTypes, blank = False, default = '', max_length = 50)

    categories = models.CharField(max_length = 500, default = '')

    start_date = models.CharField(max_length = 500, default = '')
    start_time = models.CharField(max_length = 500, default = '')
    start_full = models.CharField(max_length = 500, default = '')
    end_date = models.CharField(max_length = 500, default = '')
    end_time = models.CharField(max_length = 500, default = '')
    end_full = models.CharField(max_length = 500, default = '')

    status = models.CharField(max_length = 20, default = 'upcoming')
    # either upcoming, live, ended, or canceled

    date_created = models.DateTimeField( default = timezone.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'eid': self.id,
            'ownerid': self.ownerid,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'name': self.name,
            'desc': self.desc,
            'place': self.place,
            'location': self.location,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'link': self.link,
            'categories': self.categories,
            'start_date': self.start_date,
            'start_time': self.start_time,
            'start_full': self.start_full,
            'end_date': self.end_date,
            'end_time': self.end_time,
            'end_full': self.end_full,
            'status': self.status,
            'attendees': [a.serialize for a in EventAttendees.objects.filter(event_id = self.id)],
            'date_created': str(self.date_created),
            'last_active': str(self.last_active),
        }

    @property
    def serializeBasic(self):
        return {
            'eid': self.id,
            'ownerid': self.ownerid,
            'owner_type': self.owner_type,
            'name': self.name,
            'desc': self.desc,
            'place': self.place,
            'location': self.location,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'link': self.link,
            'categories': self.categories,
            'start_full': self.start_full,
            'end_full': self.end_full,
            'status': self.status,
            'attendees': len(EventAttendees.objects.filter(event_id = self.id)),
            'date_created': str(self.date_created),
        }

    class Meta:
        db_table = "events"

# ---


class EventAttendees(models.Model):
    OwnerType = vaults.OwnerType

    # ---

    event_id = models.IntegerField(blank = False, default = 0)
    event_rel = models.ForeignKey(Events, default = 0, related_name = "event_rel")

    attendee_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)
    attendee_id = models.IntegerField(blank = False, default = 0)

    date_created = models.DateTimeField( default = timezone.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'aid': self.id,

            'event_rel': self.event_rel.serialize,
            'event_id': self.event_id,
            'attendee': returnModelSerialized( self.attendee_type, self.attendee_id ),
            'attendee_id': self.attendee_id,
            'attendee_type': self.attendee_type,
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    class Meta:
        db_table = "event_attendees"


# ------- #
# ------- #

class Conversations(models.Model):

    owner = models.ForeignKey(Accounts, default = 0, related_name = "convo_owner")
    ownerid = models.IntegerField(blank = False, default = 0)

    name = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = timezone.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'convo_id': self.id,
            'owner': self.owner.serialize,
            'ownerid': self.ownerid,
            'name': self.name,
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    class Meta:
        db_table = "conversations"

# ---

class ConvoMembers(models.Model):

    user = models.ForeignKey(Accounts, default = 0, related_name = "convo_user")
    userid = models.IntegerField(blank = False, default = 0)

    convo_id = models.IntegerField(blank = False, default = 0)
    convo_rel = models.ForeignKey(Conversations, default = 0, related_name = "convo_member_rel")

    date_created = models.DateTimeField( default = timezone.now )
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

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
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
            'date_created': str(self.date_created)
        }

    class Meta:
        db_table = "notifications"

# ---

class Messages(models.Model):

    userA_id = models.IntegerField(blank = False, default = 0)
    userA_rel = models.ForeignKey(Accounts, default = 0, related_name = "message_user_a_rel")

    userB_id = models.IntegerField(blank = False, default = 0)
    userB_rel = models.ForeignKey(Accounts, default = 0, related_name = "message_user_b_rel")

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
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

    date_created = models.DateTimeField( default = timezone.now )
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
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    class Meta:
        db_table = "messagereplies"



# --- #
# --- #
# --- #

class Products(models.Model):
    OwnerType = vaults.OwnerType

    # ---

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    price = models.CharField(max_length = 500, blank = False, default = 0)
    name = models.CharField(max_length = 500, default = '')
    desc = models.CharField(max_length = 1500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')
    link = models.CharField(max_length = 500, default = '')

    sold = models.IntegerField(blank = False, default = 0)
    quantity = models.IntegerField(blank = False, default = 0)
    categories = models.CharField(max_length = 500, default = '')
    status = models.CharField(max_length = 125, default = '')
    # either: completed, not completed, or canceled

    unique_val = models.CharField(max_length = 125, default = randomUniqueValue )

    date_created = models.DateTimeField( default = timezone.now ) 
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'product_id': self.id,
            'unique_val': self.unique_val,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'price': self.price,
            'name': self.name,
            'desc': self.desc,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'link': self.link,
            'sold': self.sold,
            'quantity': self.quantity,
            'categories': self.categories,
            'status': self.status,
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    class Meta:
        db_table = "products"


class Services(models.Model):
    OwnerType = vaults.OwnerType
    ActiveTypes = vaults.ActiveTypes

    # ---

    ownerid = models.IntegerField(blank = False, default = 0)
    owner_type = models.CharField(choices = OwnerType, blank = False, default = '', max_length = 50)

    price = models.CharField(max_length = 500, blank = False, default = 0)
    name = models.CharField(max_length = 500, default = '')
    desc = models.CharField(max_length = 1500, default = '')
    attachment = models.CharField(max_length = 500, default = '')
    attachment_type = models.CharField(max_length = 500, default = '')
    link = models.CharField(max_length = 500, default = '')

    sold = models.IntegerField(blank = False, default = 0)
    categories = models.CharField(max_length = 500, default = '')
    status = models.CharField(max_length = 125, default = '')
    active = models.CharField(choices = ActiveTypes, blank = False, default = '', max_length = 50)
    # either: not started, penging, in progress, completed, or calceled

    unique_val = models.CharField(max_length = 125, default = randomUniqueValue )

    date_created = models.DateTimeField( default = timezone.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'service_id': self.id,
            'unique_val': self.unique_val,
            'owner': returnModelSerialized( self.owner_type , self.ownerid ),
            'owner_type': self.owner_type,
            'price': self.price,
            'name': self.name,
            'desc': self.desc,
            'attachment': self.attachment,
            'attachment_type': self.attachment_type,
            'link': self.link,
            'sold': self.sold,
            'categories': self.categories,
            'status': self.status,
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }


    class Meta:
        db_table = "services"


class Transactions(models.Model):
    ItemType = vaults.ItemType

    # ---

    item_type = models.CharField(choices = ItemType, blank = False, default = '', max_length = 50)
    item_id = models.IntegerField(blank = False, default = 0)
    item_val = models.CharField(blank = False, default = '', max_length = 50)

    customer_id = models.IntegerField(blank = False, default = 0)
    customer_rel = models.ForeignKey(Accounts, default = 0, related_name = "transactions_customer_rel")
    seller_id = models.IntegerField(blank = False, default = 0)
    seller_rel = models.ForeignKey(Accounts, default = 0, related_name = "transactions_seller_rel")

    unique_val = models.CharField(max_length = 125, default = randomUniqueValue )
    note = models.CharField(max_length = 500, default = '')
    status = models.CharField(max_length = 500, default = '')
    # either completed, not_completed, pending, or canceled

    date_created = models.DateTimeField( default = timezone.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            't_id': self.id,
            'unique_val': self.unique_val,
            'item': returnModelSerialized( self.id , self.item_type ),
            'item_type': self.item_type,
            'item_id': self.item_id,
            'item_val': self.item_val,
            'customer_id': self.customer_id,
            'customer_rel': self.customer_rel.serialize,
            'seller_id': self.seller_id,
            'seller_rel': self.seller_rel.serialize,
            'note': self.note,
            'status': self.status,
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }

    class Meta:
        db_table = "transactions"



class Feedback(models.Model):
    ItemType = vaults.ItemType
    StarType = vaults.StarType

    # ---

    transaction_id = models.IntegerField(blank = False, default = 0)
    transaction_rel = models.ForeignKey(Transactions, default = 0, related_name = "feedback_transaction_rel")

    item_type = models.CharField(choices = ItemType, blank = False, default = '', max_length = 50)
    item_id = models.IntegerField(blank = False, default = 0)
    item_val = models.CharField(blank = False, default = '', max_length = 50)

    customer_id = models.IntegerField(blank = False, default = 0)
    customer_rel = models.ForeignKey(Accounts, default = 0, related_name = "feedback_customer_rel")
    stars = models.CharField(choices = StarType, blank = False, default = '', max_length = 50)
    msg = models.CharField(max_length = 500, default = '')

    date_created = models.DateTimeField( default = timezone.now )
    last_active = models.DateTimeField(auto_now=True)

    @property
    def serialize(self):
        return {
            'feedback_id': self.id,
            'transaction_id': self.transaction_id,
            'transaction_rel': self.transaction_rel.serialize,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'item_val': self.item_val,
            'customer_id': self.customer_id,
            'customer_rel': self.customer_rel.serialize,
            'stars': self.stars,
            'msg': self.status,
            'date_created': str(self.date_created),
            'last_active': str(self.last_active)
        }


    class Meta:
        db_table = "feedback"
