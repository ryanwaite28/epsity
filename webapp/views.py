# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

import os, sys, cgi, random, string, hashlib, json
import webapp

from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_protect

from WebTools import randomVal, processImage
from models import Accounts

import routines
from vaults import webapp_dir, pages, errorPage, localPaths, serverPaths
from vaults import ALLOWED_AUDIO, ALLOWED_PHOTOS, ALLOWED_VIDEOS

# --- ----- --- #
# --- Views --- #
# --- ----- --- #

def welcome(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return redirect('/main/')
        else:
            return render(request, pages['welcome'])


# ---

@csrf_protect
def login(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return redirect('/home/')

        return render(request, pages['login'], {'error': ''},
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return routines.loginAccount(request)

# ---

@csrf_protect
def logout(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        try:
            del request.session['username']
            del request.session['email']
            request.session.flush()

            return redirect('/')

        except KeyError:
            pass

# ---

@csrf_protect
def signup(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return redirect('/home/')

        return render(request, pages['signup'], {'error': ""},
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return routines.createAccount(request)

# ---


@csrf_protect
def profileMain(request):
    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, pages['profileMain'], {'you': you},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            errorPage(request, msg)

# ---

@csrf_protect
def profileHome(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, pages['profileHome'],
                            {'you': you},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            errorPage(request, msg)

# ---

def searchEngine(request):
    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, pages['searchEngine'],
                            {'you': you},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            errorPage(request, msg)


# ---

@csrf_protect
def mySettings(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            print os.path.dirname(webapp.__file__)
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, pages['mySettings'],
                            {'you': you, 'message': ''},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            errorPage(request, msg)

# ---

@csrf_protect
def settingsAction(request):
    ''' This View Is Intended To Be Used As An AJAX & Form Handler '''

    if request.method == 'GET':
        return redirect('/mysettings')

    if request.method == 'POST':

        # Form-Data Request
        if not request.is_ajax():

            if request.POST['action'] == None:
                return JsonResponse({'msg': 'Action Message Is Missing...'})

            if request.POST['action'] == '':
                return JsonResponse({'msg': 'Action Message Is Empty/Unidentifiable...'})

            if request.POST['action'] == 'delete account':
                return routines.deleteAccount(request)

            if request.POST['action'] == 'update displayname':
                return routines.updateDisplayName(request)

            if request.POST['action'] == 'update avi link':
                return routines.updateAviLink(request)

            if request.POST['action'] == 'update wp link':
                return routines.updateWpLink(request)

            if request.POST['action'] == 'update avi file':
                return routines.updateAviFile(request)

            if request.POST['action'] == 'update wp file':
                return routines.updateWpFile(request)


            else:
                msg = 'Unknown Action...'
                errorPage(request, msg)

        # ------------ #  # ------------ #  # ------------ #

        # AJAX Request
        if request.is_ajax():
            try:
                data = json.loads(request.body)

                if data['action'] == None:
                    return JsonResponse({'msg': 'Action Message Is Missing...'})

                if data['action'] == '':
                    return JsonResponse({'msg': 'Action Message Is Empty/Unidentifiable...'})



                if data['action'] == 'update bio':
                    if data['bio'] == '' or data['bio'] == None:
                        return routines.updateAccountBio(request, 'No Bio...')

                    return routines.updateAccountBio(request, data['bio'])

                if data['action'] == 'update interests':
                    return routines.updateAccountInterests(request, data['str'])

                if data['action'] == 'update seeking':
                    return routines.updateAccountSeeking(request, data['str'])

                if data['action'] == 'load settings lists':
                    return routines.loadSettingsLists(request)


            except KeyError, AttributeError:
                return JsonResponse({'msg': 'Failed To Load JSON Data...'})

# ---
