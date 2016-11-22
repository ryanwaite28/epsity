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


current_dir = os.path.dirname(os.path.abspath(__file__))

ALLOWED_PHOTOS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_VIDEOS = set(['mp4', 'avi', 'mov'])
ALLOWED_AUDIO = set(['mp3', 'wav'])

def allowed_photo(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_PHOTOS

def allowed_video(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_VIDEOS

def allowed_audio(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_AUDIO

# Dictionary of all pages/views for easy and dynamic rendering.
pages = {
    'welcome': 'welcome.html',
    'error': 'error.html',
    'login': 'login.html',
    'signup': 'signup.html',
    'mySettings': 'user-settings.html',
    'searchEngine': 'search-1.html',
    'profileMain': 'profile-main.html',
    'profileHome': 'profile-home.html',
    'profilePosts': 'profile-posts.html',
    'profilePhoto': 'profile-photo.html',
    'profileVideo': 'profile-video.html',
    'profileAudio': 'profile-audio.html',
}

localPaths = {
    'avatars': current_dir + '/static/avatars/',
    'backgrounds': current_dir + '/static/backgrounds/',
    'avatars_rel': '/static/avatars/',
    'backgrounds_rel': '/static/backgrounds/',
    'images_rel': '/static/img/'
}

serverPaths = {

}

def errorPage(request, msg = None):
    if msg == None or msg == '' or request.method == 'POST':
        print '--- Error Page Redirecting...'
        return redirect('/')

    string = randomVal()
    return render(request, pages['error'],
                    {'errorMessage': msg, 'value': string})

# ---
