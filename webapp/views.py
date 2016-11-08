# --- Imports --- #

import os, sys, cgi, random, string, hashlib
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect

from WebTools import randomVal, uploadImage, processImage, generateState
from models import Accounts

# --- Setup Code --- #

# Dictionary of all pages/views for easy and dynamic rendering.
pages = {
    'welcome': 'welcome.html',
    'login': 'login.html',
    'signup': 'signup.html',
    #
    'profileMain': 'profile-main.html',
    'profileHome': 'profile-home.html',
    'profilePosts': 'profile-posts.html',
    'profilePhoto': 'profile-photo.html',
    'profileVideo': 'profile-video.html',
    'profileAudio': 'profile-audio.html',
}

# --- Views --- #

def welcome(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return redirect('/home/')
        else:
            return render(request, pages['welcome'])

# ---

@csrf_protect
def login(request):
    if request.method == 'GET':
        return render(request, pages['login'], {'error': ''})

    if request.method == 'POST':
        try:
            email = request.POST['email']
            pswrd = request.POST['pswrd']

            you = Users.objects.get( email=email, pswrd=pswrd )

            request.session['username'] = you.uname
            request.session['email'] = you.email

            return redirect('/home/')

        except ObjectDoesNotExist:
            return render(request, loginPage, {'error': "Incorrect info"})

# ---

# @csrf_protect
def logout(request):
    if request.method == 'GET':
        try:
            del request.session['username']
            del request.session['email']
            request.session.flush()
            print 'ok'
        except KeyError:
            pass

        return redirect('/')

# ---

@csrf_protect
def signup(request):
    if request.method == 'GET':
        return render(request, pages['signup'], context_instance=RequestContext(request))

    if request.method == 'POST':
        try:
            uname = cgi.escape( request.POST['uname'] )
            displayName = request.POST['displayname']
            email = request.POST['email']
            provider = request.POST['provider']
            provider_id = request.POST['providerid']
            img = request.POST['image']
            pswrd = hashlib.md5( request.POST['uid'] ).hexdigest()

            checkEmail = Accounts.objects.get(email=email)
            if checkEmail != None:
                return

            checkUsername = Accounts.objects.get(uname=uname)
            if checkUsername != None:
                return

            newUser = Accounts(uname=uname, displayname=displayName, img=img,
                            provider=provider, provider_id=provider_id,
                            email=email, pswrd=pswrd)
            newUser.save()

            request.session['username'] = uname
            request.session['email'] = email

            return redirect('/home/')

        except ObjectDoesNotExist:
            return render(request, loginPage, {'error': "Incorrect info"})

# ---


@csrf_protect
def profileMain(request):
    if request.method == 'GET':
        return render(request, pages['profileMain'], context_instance=RequestContext(request))

# ---

@csrf_protect
def profileHome(request):
    if request.method == 'GET':
        return render(request, pages['profileHome'], context_instance=RequestContext(request))

# ---
