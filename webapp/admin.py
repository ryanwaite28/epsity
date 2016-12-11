from django.contrib import admin

from models import Accounts, AviModel, WpModel, Groups, GroupMembers
from models import Follows, FollowRequests
from models import GroupRequests, GroupInvitations, Messages, MessageReply
from models import mediaPhotoModel, mediaVideoModel, mediaAudioModel
from models import Posts, Comments, Replies, Likes

# Register your models here.

admin.site.register(Accounts)
