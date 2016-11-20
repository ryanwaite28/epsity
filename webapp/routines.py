# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

import os, sys, cgi, random, string, hashlib, json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template import RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_protect

from WebTools import randomVal, uploadImage, processImage, generateState
from models import Accounts

from vaults import pages

# --- -------- --- #
# --- Routines --- #
# --- -------- --- #



def errorPage(request, msg=None):
    if msg == None or msg == '' or request.method == 'POST':
        print '--- Error Page Redirecting...'
        return redirect('/')

    return render(request,
                    {'errorMessage', msg},
                    pages['error'])


def loginAccount(request):
    try:
        email = request.POST['email']
        provider_id = request.POST['providerid']
        pswrd = hashlib.sha256( request.POST['uid'] ).hexdigest()

        you = Accounts.objects.filter( email=email, pswrd=pswrd ).first()
        if you == None:
            chance = Accounts.objects.filter( pswrd=pswrd ).first()
            if chance == None:
                return render(request, pages['login'],
                                {'error': 'Incorrect Info.'},
                                context_instance=RequestContext(request))

        request.session['username'] = you.uname
        request.session['email'] = you.email

        return redirect('/home/')

    except ObjectDoesNotExist:
        return render(request, pages['login'], {'error': 'Incorrect Info.'},
                        context_instance=RequestContext(request))



def createAccount(request):
    try:
        uname = cgi.escape( request.POST['uname'] )
        displayName = request.POST['displayname']
        email = request.POST['email']
        provider = request.POST['provider']
        provider_id = request.POST['providerid']
        img = request.POST['image']
        pswrd = hashlib.sha256( request.POST['uid'] ).hexdigest()

        checkEmail = Accounts.objects.filter(email=email).first()
        if checkEmail != None:
            return render(request,
                            pages['signup'],
                            {'error': "That Email Is Already In Use."},
                            context_instance=RequestContext(request))

        checkUsername = Accounts.objects.filter(uname=uname).first()
        if checkUsername != None:
            return render(request,
                            pages['signup'],
                            {'error': "That Username Is Already In Use."},
                            context_instance=RequestContext(request))

        newUser = Accounts(uname=uname, displayname=displayName, avi=img,
                        provider=provider, provider_id=provider_id,
                        email=email, pswrd=pswrd)
        newUser.save()

        request.session['username'] = uname
        request.session['email'] = email

        return redirect('/home/')

    except MultipleObjectsReturned:
        return render(request,
                        pages['signup'],
                        {'error': "There Was An Error. Please Try Again."},
                        context_instance=RequestContext(request))


def deleteAccount(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        errorPage(request, msg)



def updateAccountBio(request, content):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.bio_desc = cgi.escape(content)
        you.save( update_fields=['bio_desc'] )


        return JsonResponse({'msg':'successful', 'bio':content})

    except ObjectDoesNotExist:
        error = 'User Account Not Found.'
        return JsonResponse({'msg':'unsuccessful - error', 'error': msg})


def updateAccountInterests(request, content):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.interests = cgi.escape(content)
        you.save( update_fields=['interests'] )


        return JsonResponse({'msg':'successful', 'interests':content.split()})

    except ObjectDoesNotExist:
        error = 'User Account Not Found.'
        return JsonResponse({'msg':'unsuccessful - error', 'error': msg})


def updateAccountSeeking(request, content):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.seeking = cgi.escape(content)
        you.save( update_fields=['seeking'] )


        return JsonResponse({'msg':'successful', 'seeking':content.split()})

    except ObjectDoesNotExist:
        error = 'User Account Not Found.'
        return JsonResponse({'msg':'unsuccessful - error', 'error': msg})



def loadSettingsLists(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])

        resp = {
            'msg': 'lists',
            'interests': you.interests.split(),
            'seeking': you.seeking.split()
        }

        return JsonResponse(resp)

    except ObjectDoesNotExist:
        error = 'User Account Not Found.'
        return JsonResponse({'msg':'unsuccessful - error', 'error': msg})
