# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

import os, sys, cgi, random, string, hashlib
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_protect

from WebTools import randomVal, uploadImage, processImage, generateState
from models import Accounts

import routines
from vaults import pages

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

def errorPage(request, msg=None):
    if msg == None or msg == '' or request.method == 'POST':
        print '--- Error Page Redirecting...'
        return redirect('/')

    return render(request,
                    {'errorMessage', msg},
                    pages['error'])


# ---

@csrf_protect
def login(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return redirect('/home/')

        return render(request,
                        pages['login'],
                        {'error': ''},
                        context_instance=RequestContext(request))

    if request.method == 'POST':
        routines.loginAccount(request)

# ---

# @csrf_protect
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

        return render(request,
                        pages['signup'],
                        {'error': ""},
                        context_instance=RequestContext(request))

    if request.method == 'POST':
        routines.createAccount(request)

# ---


@csrf_protect
def profileMain(request):
    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])
            # print you.serialize_basic
            return render(request,
                            pages['profileMain'],
                            {'you': you},
                            context_instance=RequestContext(request))

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
            # print you.serialize_basic
            return render(request,
                            pages['profileHome'],
                            {'you': you},
                            context_instance=RequestContext(request))

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
            you = Accounts.objects.get(uname = request.session['username'])
            # print you.serialize_basic
            return render(request,
                            pages['mySettings'],
                            {'you': you},
                            context_instance=RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            errorPage(request, msg)

# ---

@csrf_protect
def deleteAccount(request):
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        routines.deleteAccount(request)

# ---
