# --- --- --- --- --- #
# --- Helper Code --- #
# --- --- --- --- --- #

import os, sys, cgi, random, string, hashlib, json
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

# Dictionary of all pages/views for easy and dynamic rendering.
pages = {
    'welcome': 'welcome.html',
    'error': 'error.html',
    'generic': 'generic-1.html',
    'login': 'login.html',
    'signup': 'signup.html',
    'createview': 'create-1.html',
    'notificationsView': 'notifications-1.html',
    'mySettings': 'user-settings.html',
    'messagesView': 'messages-1.html',
    'searchEngine': 'search-1.html',
    'profileMain': 'profile-main.html',
    'profileHome': 'profile-home.html',
    'UserPage': 'user-page-view.html',
    'GroupPage': 'group-page-view.html',
    'profilePosts': 'profile-posts.html',
    'profilePhoto': 'profile-photo.html',
    'profileVideo': 'profile-video.html',
    'profileAudio': 'profile-audio.html',
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

ownerTypes = {
    'account': 'Account',
    'group': 'Group'
}

mediaTypes = {
    'photo': 'Photo',
    'audio': 'Audio',
    'video': 'Video'
}


# Master Dictionary
masterDICT = {
    'pages': pages,
    'localPaths': localPaths,
    'serverPaths': serverPaths,
    'followStates': followStates,
    'groupStates': groupStates,
    'postTypes': postTypes,
    'ownerTypes': ownerTypes,
    'mediaTypes': mediaTypes,
}

# --- #

def processFileUpload(file):
    '''  '''

def errorPage(request, msg = None):
    if msg == None or msg == '' or request.method == 'POST':
        # print '--- Error Page Redirecting...'
        return redirect('/')

    string = randomVal()
    return render(request,
                    pages['error'],
                    {'errorMessage': msg,
                    'value': string})


def genericPage(request, msg, redirect):

    string = randomVal()
    return render(request,
                    pages['generic'],
                    {'message': msg,
                    'redirect': redirect,
                    'value': string})
