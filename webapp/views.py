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
from models import Accounts, Groups, GroupMembers, Follows, FollowRequests

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
            return errorPage(request, msg)

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
            followers = Follows.objects.filter(follow_id=you.id)
            following = Follows.objects.filter(userid=you.id)
            groups = GroupMembers.objects.filter(userid=you.id)

            return render(request, pages['profileHome'],
                            {'you': you,
                            'info': you.get_info,
                            'followers': len(followers),
                            'following': len(following),
                            'groups': len(groups)},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
def userPage(request, query):
    if request.method == 'GET':
        # print query
        try:
            if 'username' in request.session:
                you = Accounts.objects.get(uname = request.session['username'])
            else:
                you = None

            user = Accounts.objects \
            .filter(uname__iexact = query).first()

            followers = Follows.objects.filter(follow_id=user.id)
            following = Follows.objects.filter(userid=user.id)
            groups = GroupMembers.objects.filter(userid=user.id)

            if user == None:
                msg = 'User Account Not Found.'
                return errorPage(request, msg)

            else:
                if 'username' in request.session:
                    if user.uname == request.session['username']:
                        return redirect('/home')

                    else:
                        return render(request,
                                        pages['UserPage'],
                                        {'you': you,
                                        'user': user,
                                        'info': user.get_info,
                                        'followers': len(followers),
                                        'following': len(following),
                                        'groups': len(groups)},
                                        context_instance = RequestContext(request))
                else:
                    return render(request,
                                    pages['UserPage'],
                                    {'you': you,
                                    'user': user,
                                    'info': user.get_info,
                                    'followers': len(followers),
                                    'following': len(following),
                                    'groups': len(groups)},
                                    context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
def groupPage(request, query):
    if request.method == 'GET':
        # print query
        try:
            if 'username' in request.session:
                you = Accounts.objects.get(uname = request.session['username'])
            else:
                you = None

            group = Groups.objects \
            .filter(uname__iexact = query).first()

            if group == None:
                msg = 'Group Not Found.'
                return errorPage(request, msg)

            else:
                return render(request,
                                pages['GroupPage'],
                                {'you': you,
                                'group': group},
                                context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
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
            return errorPage(request, msg)


    if request.method == 'POST':
        data = json.loads(request.body)

        if data['action'] == 'search query':
            return routines.searchEngine(request)

        if data['action'] == 'search for members':
            return routines.searchForMembers(request)

# ---

@csrf_protect
def mySettings(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            # print os.path.dirname(webapp.__file__)
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, pages['mySettings'],
                            {'you': you, 'message': ''},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
def createView(request):

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, pages['createview'],
                            {'you': you, 'message': ''},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

    # --- #

    if request.method == 'POST':

        # Form-Data Request
        if not request.is_ajax():

            if request.POST['action'] == None:
                return render(request, pages['createview'],
                                {'you': you, 'message': 'Action Is Missing...'},
                                context_instance = RequestContext(request))

            if request.POST['action'] == '':
                return render(request, pages['createview'],
                                {'you': you, 'message': 'Action Is Unknown...'},
                                context_instance = RequestContext(request))

            if request.POST['action'] == 'create group':
                return routines.createGroup(request)

            else:
                msg = 'Unknown Action...'
                return errorPage(request, msg)

        # ------------ #  # ------------ #  # ------------ #

        # AJAX Request
        if request.is_ajax():
            try:
                data = json.loads(request.body)

                if data['action'] == None:
                    msg = {'msg': 'Action Message Is Missing...'}
                    return JsonResponse(msg)

                if data['action'] == '':
                    msg = {'msg': 'Action Message Is Empty/Unidentifiable...'}
                    return JsonResponse(msg)



            except KeyError, AttributeError:
                return JsonResponse({'msg': 'Failed To Load JSON Data...'})


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
                return render(request, pages['mySettings'],
                                {'you': you, 'message': 'Action Message Missing...'},
                                context_instance = RequestContext(request))

            if request.POST['action'] == '':
                return render(request, pages['mySettings'],
                                {'you': you, 'message': 'Action Is Unknown...'},
                                context_instance = RequestContext(request))

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

            if request.POST['action'] == 'update group':
                return routines.updateGroup(request)

            if request.POST['action'] == 'update account status':
                return routines.editAccountStatus(request)

            if request.POST['action'] == 'delete group':
                return routines.deleteGroup(request)

            else:
                msg = 'Unknown Action...'
                return errorPage(request, msg)

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

@csrf_protect
def checkPoint(request):
    ''' This View Function Is Intended To Be Called By AJAX Requests '''
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if data['action'] == None:
                return JsonResponse({'msg': 'Action Message Is Missing...'})

            if data['action'] == '':
                return JsonResponse({'msg': 'Action Message Is Empty/Unidentifiable...'})

            # ----- #

            if data['action'] == 'check group uname':
                return routines.checkGroupUserName(request, data)

        except:
            return JsonResponse({'msg': 'Failed To Load JSON Data...'})


# ---

@csrf_protect
def userAction(request):
    ''' This View Function Is Intended To Be Called By AJAX Requests '''
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # ----- #

            if data['action'] == None:
                return JsonResponse({'msg': 'Action Message Is Missing...'})

            if data['action'] == '':
                return JsonResponse({'msg': 'Action Message Is Empty/Unidentifiable...'})

            # ----- #

            if data['action'] == 'followUser':
                return routines.followUser(request, data)

            if data['action'] == 'unfollowUser':
                return routines.unfollowUser(request, data)

            if data['action'] == 'cancelPendingFollow':
                return routines.cancelPendingFollow(request, data)

            if data['action'] == 'accept follow':
                return routines.acceptFollow(request, data)

            if data['action'] == 'decline follow':
                return routines.declineFollow(request, data)

            # ---

            if data['action'] == 'sendGroupInvitation':
                return routines.sendGroupInvitation(request, data)

            if data['action'] == 'cancelPendingGroupInvite':
                return routines.cancelPendingGroupInvite(request, data)

            if data['action'] == 'accept group invite':
                return routines.acceptGroupInvitation(request, data)

            if data['action'] == 'decline group invite':
                return routines.declineGroupInvitation(request, data)

            if data['action'] == 'removeMember':
                return routines.removeGroupMember(request, data)

            # ---

            if data['action'] == 'load notes all':
                return routines.loadNotesAll(request, data)

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

def notificationsView(request):
    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, pages['notificationsView'],
                            {'you': you, 'message': ''},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)
