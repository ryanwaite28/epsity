# --- --- --- --- --- #
# --- Helper Code --- #
# --- --- --- --- --- #

import bcrypt
import os, sys, cgi, random, string, hashlib, json, requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template import RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_protect

from WebTools import randomVal, processImage

# --- #

webapp_dir = os.path.dirname(os.path.abspath(__file__))
hashSalt = 'C9RUbql6IDHIYoJ'

ALLOWED_PHOTOS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_VIDEOS = set(['mp4', 'avi', 'mov', 'webm', 'oog'])
ALLOWED_AUDIO = set(['mp3', 'wav'])

ALLOWED_MEDIA = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm', 'oog' 'mp3', 'wav'])

def allowed_photo(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_PHOTOS

def allowed_video(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_VIDEOS

def allowed_audio(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_AUDIO



def allowed_media(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_MEDIA



# Instance Tuple Variables For Model Classes

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

PostStatuses = (
    ('public', 'public'),
    ('private', 'private'),
    ('personal', 'personal'),
    ('deleted', 'deleted'),
)

ContentType = (
    ('Post', 'Post'),
    ('Comment', 'Comment'),
    ('Reply', 'Reply'),
    ('Group', 'Group'),
    ('Event', 'Event'),
    ('SharePost', 'SharePost'),
)

AttachmentTypes = (
    ('Photo', 'Photo'),
    ('Audio', 'Audio'),
    ('Video', 'Video'),
)

ItemType = (
    ('Account', 'Account'),
    ('Group', 'Group'),
    ('Product', 'Product'),
    ('Service', 'Service'),
    ('Event', 'Event'),
    ('Post', 'Post'),
    ('SharePost', 'SharePost'),
)

StarType = (
    ('One', 'One'),
    ('Two', 'Two'),
    ('Three', 'Three'),
    ('Four', 'Four'),
    ('Five', 'Five'),
)

FeaturedStatus = (
    ('Live', 'Live'),
    ('Expired', 'Expired'),
)

FeaturedType = (
    ('Day', 'Day'),
    ('Week', 'Week'),
    ('Month', 'Month'),
)

ActiveTypes = (
    ('Available', 'Available'),
    ('Unavailable', 'Unavailable')
)

# Dictionary of all pages/views for easy and dynamic rendering.
pages = {
    'welcome': 'welcome.html',
    'discoverView': 'discover-1.html',
    'newestView': 'newest-1.html',
    'trendingView': 'trending-1.html',
    'featuredView': 'featured-1.html',
    'error': 'error.html',
    'generic': 'generic-1.html',
    'login': 'login.html',
    'signup': 'signup.html',
    'createview': 'create-1.html',
    'notificationsView': 'notifications-1.html',
    'mySettings': 'user-settings.html',
    'eventsview': 'events-1.html',
    'eventview': 'events-2.html',
    'productView': 'products-1.html',
    'serviceView': 'services-1.html',
    'messagesView': 'messages-1.html',
    'conversationsView': 'conversations-1.html',
    'searchEngine': 'search-1.html',
    'searchView': 'search-2.html',
    'dashboard': 'profile-main.html',
    'profileHome': 'profile-home.html',
    'UserPage': 'user-page-view.html',
    'GroupPage': 'group-page-view.html',
    'postView': 'post-view-1.html',
    'profilePosts': 'profile-posts.html',
    'profilePhoto': 'profile-photo.html',
    'profileVideo': 'profile-video.html',
    'profileAudio': 'profile-audio.html',

    'new_post': 'new-post-1.html',
    'new_comment': 'new-comment-1.html',
    'new_reply': 'new-reply-1.html',

    'testing': 'testing-1.html'
}

localPaths = {
    'avatars': webapp_dir + '/static/avatars/',
    'backgrounds': webapp_dir + '/static/backgrounds/',
    'avatars_rel': '/static/avatars/',
    'backgrounds_rel': '/static/backgrounds/',
    'images_rel': '/static/img/'
}

serverPaths = {

}

followStates = {
    'pending': {
        'status': 'Pending Follow',
        'btn': 'default',
        'msg': 'Pending',
        'action': 'cancelPendingFollow',
        'title': 'Cancel Pending'
    },
    'following': {
        'status': 'Currently Following',
        'btn': 'warning',
        'msg': 'Unfollow',
        'action': 'unfollowUser',
        'title': 'Unfollow User'
    },
    'not_following': {
        'status': 'Not Following',
        'btn': 'success',
        'msg': 'Follow',
        'action': 'followUser',
        'title': 'Follow User'
    },
    'options': {
        'accept': 'acceptFollow',
        'decline': 'declineFollow'
    }
}

groupStates = {
    'owner': {
        'pending': {
            'status': 'pending invite',
            'btn': 'default',
            'msg': 'Pending',
            'action': 'cancelPendingGroupInvite',
            'title': 'Cancel Pending Group Invite'
        },
        'member': {
            'status': 'currently a member',
            'btn': 'warning',
            'msg': 'Remove Member',
            'action': 'removeMember',
            'title': 'Remove From Group'
        },
        'not_member': {
            'status': 'not a member',
            'btn': 'success',
            'msg': 'Send Group Invite',
            'action': 'sendGroupInvitation',
            'title': 'Send Group Invite'
        },
        'options': {
            'accept': 'acceptGroupRequest',
            'decline': 'declineGroupRequest'
        }
    },

    'user': {
        'pending': {
            'status': 'Pending Invite',
            'btn': 'default',
            'msg': 'Pending',
            'action': 'cancelPendingGroupRequest',
            'title': 'Cancel Pending Group Invite'
        },
        'member': {
            'status': 'Currently A Member',
            'btn': 'warning',
            'msg': 'Leave Group',
            'action': 'leaveGroup',
            'title': 'Leave Group'
        },
        'not_member': {
            'status': 'Not A Member',
            'btn': 'success',
            'msg': 'Request Invite',
            'action': 'requestGroupInvite',
            'title': 'Request Group Invite'
        },
        'options': {
            'accept': 'acceptGroupInvite',
            'decline': 'declineGroupInvite'
        }
    }
}

postTypes = {
    'text': 'Text',
    'photo': 'Photo',
    'audio': 'Audio',
    'video': 'Video',
    'link': 'Link'
}
postStatuses = {
    'public': 'public',
    'private': 'private',
    'personal': 'personal'
}

ownerTypes = {
    'account': 'Account',
    'group': 'Group'
}

mediaTypes = {
    'photo': 'Photo',
    'audio': 'Audio',
    'video': 'Video'
}

contentTypes = {
    'post': 'Post',
    'comment': 'Comment',
    'reply': 'Reply',
    'event': 'Event',
    'sharepost': 'SharePost',
}

statuses = {
    'like': {
        'liked': {
            'msg': 'not_liked',
            'text': 'Liked',
            'action': 'unlike',
            'class': 'like-btn-f'
        },
        'not_liked': {
            'msg': 'not_liked',
            'text': 'Like',
            'action': 'like',
            'class': 'like-btn-o'
        }
    },

    'event': {
        'upcoming': 'upcoming',
        'live': 'live',
        'ended': 'ended',
        'canceled': 'canceled',
    },

    'transaction': {
        'completed': 'completed',
        'not_completed': 'not_completed',
        'pending': 'pending',
        'canceled': 'canceled'
    }
}

fetchType = {
    'posts': {
        'main': 'main',
        'home': 'home',
        'user': 'user',
        'group': 'group',
        'account': 'account'
    }
}

starType = {
    'One': 'One',
    'Two': 'Two',
    'Three': 'Three',
    'Four': 'Four',
    'Five': 'Five'
}

itemTypes = {
    'account': 'Account',
    'group': 'Group',
    'product': 'Product',
    'service': 'Service',
    'event': 'Event',
    'post': 'Post',
    'sharepost': 'SharePost',
}

featuredStatus = {
    'live': 'Live',
    'expired': 'Expired',
}

featuredType = {
    'day': 'Day',
    'week': 'Week',
    'month': 'Month',
}

activeTypes = {
    'availavle': 'Available',
    'unavailable': 'Unavailable',
}

# Master Dictionary
masterDICT = {
    'pages': pages,
    'localPaths': localPaths,
    'serverPaths': serverPaths,
    'followStates': followStates,
    'groupStates': groupStates,
    'postTypes': postTypes,
    'postStatuses': postStatuses,
    'ownerTypes': ownerTypes,
    'mediaTypes': mediaTypes,
    'contentTypes': contentTypes,
    'statuses': statuses,
    'fetchType': fetchType,
    'starType': starType,
    'itemTypes': itemTypes,
    'featuredStatus': featuredStatus,
    'featuredType': featuredType,
    'activeTypes': activeTypes
}

# --- #
