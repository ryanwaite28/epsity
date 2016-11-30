# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

import os, sys, cgi, random, string, hashlib, json
import webapp

from django import forms
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template import RequestContext
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

from WebTools import randomVal, processImage, saveImageLocal
from models import Accounts, AviModel, WpModel, Groups, GroupMembers
from models import Follows, FollowRequests

from vaults import webapp_dir, pages, errorPage, localPaths, serverPaths
from vaults import ALLOWED_AUDIO, ALLOWED_PHOTOS, ALLOWED_VIDEOS
from vaults import allowed_audio, allowed_photo, allowed_audio


# --- -------- --- #
# --- Routines --- #
# --- -------- --- #


def loginAccount(request):
    try:
        email = request.POST['email']
        provider_id = request.POST['providerid']
        pswrd = hashlib.sha256( request.POST['uid'] ).hexdigest()

        you = Accounts.objects.filter( email=email ).first()
        if you == None:
            return render(request,
                            pages['login'],
                            {'error': 'Incorrect Info.'},
                            context_instance=RequestContext(request))

        request.session['username'] = you.uname
        request.session['email'] = you.email

        return redirect('/home/')

    except ObjectDoesNotExist:
        return render(request,
                        pages['login'],
                        {'error': 'Incorrect Info.'},
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

        newUser = Accounts(uname=uname,
                            displayname=displayName,
                            avi=img,
                            provider=provider,
                            provider_id=provider_id,
                            email=email,
                            pswrd=pswrd)

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
        you.delete()

        del request.session['username']
        del request.session['email']
        request.session.flush()

        return redirect('/')

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



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


        return JsonResponse({'msg':'successful', 'interests':content.split(';')})

    except ObjectDoesNotExist:
        error = 'User Account Not Found.'
        return JsonResponse({'msg':'unsuccessful - error', 'error': msg})


def updateAccountSeeking(request, content):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.seeking = cgi.escape(content)
        you.save( update_fields=['seeking'] )


        return JsonResponse({'msg':'successful', 'seeking':content.split(';')})

    except ObjectDoesNotExist:
        error = 'User Account Not Found.'
        return JsonResponse({'msg':'unsuccessful - error', 'error': msg})



def loadSettingsLists(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        groups = Groups.objects.filter(ownerid = you.id).all()

        resp = {
            'msg': 'lists',
            'interests': you.interests.split(';'),
            'seeking': you.seeking.split(';'),
            'groups': [g.serialize for g in groups]
        }

        return JsonResponse(resp)

    except ObjectDoesNotExist:
        error = 'User Account Not Found.'
        return JsonResponse({'msg':'unsuccessful - error', 'error': msg})

def updateDisplayName(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.displayname = cgi.escape( request.POST['displayname'] )
        you.save( update_fields=['displayname'] )

        return render(request,
                    pages['mySettings'],
                    {'you': you,
                    'message': "Displayname Updated Successfully!"},
                    context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def editAccountStatus(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.status = request.POST['select']
        you.save( update_fields=['status'] )

        print you.status

        return render(request,
                    pages['mySettings'],
                    {'you': you,
                    'message': "Status Updated Successfully!"},
                    context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def updateAviLink(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.avi = cgi.escape( request.POST['avi'] )
        you.save( update_fields=['avi'] )

        return render(request,
                    pages['mySettings'],
                    {'you': you, 'message': "Avatar Updated Successfully!"},
                    context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def updateWpLink(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        you.background = cgi.escape( request.POST['background'] )
        you.save( update_fields=['background'] )

        return render(request,
                    pages['mySettings'],
                    {'you': you, 'message': "Wallpaper Updated Successfully!"},
                    context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def updateAviFile(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        file = request.FILES['imageFile']

        if file and file.name != '' and allowed_photo(file.name):
            newdoc = AviModel(docfile = request.FILES['imageFile'])
            newdoc.save()
            you.avi = newdoc.docfile.url
            you.save( update_fields=['avi'] )

            return render(request,
                        pages['mySettings'],
                        {'you': you,
                        'message': "Avatar Updated Successfully!"},
                        context_instance=RequestContext(request))

        else:
            return render(request,
                        pages['mySettings'],
                        {'you': you,
                        'message': "Error - That Was Not An Image File."},
                        context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)

def updateWpFile(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        file = request.FILES['imageFile']

        if file and file.name != '' and allowed_photo(file.name):
            newdoc = WpModel(docfile = request.FILES['imageFile'])
            newdoc.save()
            you.background = newdoc.docfile.url
            you.save( update_fields=['background'] )

            return render(request,
                        pages['mySettings'],
                        {'you': you,
                        'message': "Wallpaper Updated Successfully!"},
                        context_instance=RequestContext(request))

        else:
            return render(request,
                        pages['mySettings'],
                        {'you': you,
                        'message': "Error - That Was Not An Image File."},
                        context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def searchEngine(request):
    data = json.loads(request.body)
    you = Accounts.objects.get(uname = request.session['username'])
    # print data

    if data['query'] == None:
        return JsonResponse({'msg': 'Query Is Missing...'})

    if data['query'] == '':
        return JsonResponse({'msg': 'Query Is Empty/Unidentifiable...'})

    users = Accounts.objects.exclude(id = you.id) \
    .filter(uname__contains = data['query'])[:10]
    groups = Groups.objects.filter(uname__contains = data['query'])[:10]

    users = [u.serialize for u in users]
    groups = [g.serialize for g in groups]

    for u in users:
        checkFollow = Follows.objects \
        .filter(userid = you.id, follow_id = u['userid']).first()

        if checkFollow == None:
            checkFollowRequest = FollowRequests.objects \
            .filter(sender_id=you.id , recipient_id=u['userid']).first()

            if checkFollowRequest != None:
                u['status'] = 'Pending Follow'
                u['btn'] = 'default'
                u['msg'] = 'Pending'
                u['action'] = 'cancelPending'
                u['title'] = 'Cancel Pending'

            else:
                u['status'] = 'Not Following'
                u['btn'] = 'success'
                u['msg'] = 'Follow'
                u['action'] = 'followUser'
                u['title'] = 'Follow User'

        if checkFollow != None:
            u['status'] = 'Currently Following'
            u['btn'] = 'warning'
            u['msg'] = 'Unfollow'
            u['action'] = 'unfollowUser'
            u['title'] = 'Unfollow User'

    # print users

    for g in groups:
        checkMembership = GroupMembers.objects \
        .filter(group_id = g['gid'], userid = you.id).first()

        if checkMembership == None:
            g['status'] = 'Not A Member'
            g['btn'] = 'success'
            g['msg'] = 'Request Invitation'
            g['action'] = 'requestGroupInvitation'

        else:
            g['status'] = 'Currently A Member'
            g['btn'] = 'warning'
            g['msg'] = 'Leave Group'
            g['action'] = 'leaveGroup'

    # print groups

    resp = {
        'msg': 'search query',
        'users': users,
        'groups': groups
    }

    return JsonResponse(resp)

# ---

def searchForMembers(request):
    data = json.loads(request.body)
    you = Accounts.objects.get(uname = request.session['username'])
    group = Groups.objects.filter(id = data['gid']).first()

    if group == None:
        return JsonResponse({'msg': 'Group Could Not Be Loaded...'})

    if data['query'] == None:
        return JsonResponse({'msg': 'Query Is Missing...'})

    if data['query'] == '':
        return JsonResponse({'msg': 'Query Is Empty/Unidentifiable...'})

    if data['limit'] == None or data['limit'] == '' or data['limit'] >= 30:
        data['limit'] = 15

    users = Accounts.objects \
    .exclude(id = you.id) \
    .filter(uname__contains = data['query'])[:data['limit']]

    users = [u.serialize for u in users]
    # print len(users)

    for u in users:
        checkMembership = GroupMembers.objects \
        .filter(group_id = data['gid'], userid = u['userid']).first()

        if checkMembership == None:
            u['status'] = 'Not A Member'
            u['btn'] = 'success'
            u['msg'] = 'Send Invitation!'
            u['action'] = 'sendGroupInvitation'

        else:
            u['status'] = 'Currently A Member'
            u['btn'] = 'default'
            u['msg'] = 'Currently A Member'
            u['action'] = 'Remove Member'

    print users

    resp = {
        'msg': 'search results',
        'users': users,
    }

    return JsonResponse(resp)

# ---

def checkGroupUserName(request, data):
    if data['groupUserName'][-1] == ' ':
        data['groupUserName'] = data['groupUserName'][:-1]
    checkGroup = Groups.objects \
    .filter(uname__iexact = data['groupUserName']).first()
    if checkGroup != None:
        return JsonResponse({'msg': 'taken'})

    else:
        return JsonResponse({'msg': 'available'})

# ---

def createGroup(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])

        checkGroup = Groups.objects \
        .filter(uname = request.POST['uname']).first()
        if checkGroup != None:
            return render(request,
                        pages['createview'],
                        {'you': you,
                        'message': "That Group Name Is Already In Use!"},
                        context_instance=RequestContext(request))

        if request.POST['displayname'][-1] == ' ':
            request.POST['displayname'] = request.POST['displayname'][:-1]

        newGroup = Groups(owner_rel=you,
                            ownerid=you.id,
                            displayname=request.POST['displayname'],
                            uname=request.POST['uname'].lower(),
                            desc=request.POST['desc'])
        newGroup.save()

        if request.FILES:
            group = Groups.objects.filter(id = newGroup.id).first()

            aviFile = request.FILES['imageFileAvi']
            wpFile = request.FILES['imageFileWp']

            if not aviFile or \
            aviFile.name == '' or \
            not allowed_photo(aviFile.name):
                return render(request,
                            pages['createview'],
                            {'you': you,
                            'message': 'Error - Bad Avatar File Input...'},
                            context_instance=RequestContext(request))

            if not wpFile or \
            wpFile.name == '' or \
            not allowed_photo(wpFile.name):
                return render(request,
                            pages['createview'],
                            {'you': you,
                            'message': 'Error - Bad Wallpaper File Input...'},
                            context_instance=RequestContext(request))

            if aviFile and aviFile.name != '' and allowed_photo(aviFile.name):
                newdoc = AviModel(docfile = request.FILES['imageFileAvi'])
                newdoc.save()
                group.avi = newdoc.docfile.url

            if wpFile and wpFile.name != '' and allowed_photo(wpFile.name):
                newdoc = WpModel(docfile = request.FILES['imageFileWp'])
                newdoc.save()
                group.background = newdoc.docfile.url

            group.save()

            # print group
            # print group.serialize

        return render(request,
                    pages['createview'],
                    {'you': you, 'message': "New Group Created!"},
                    context_instance=RequestContext(request))


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)

# ---

def updateGroup(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])

        group = Groups.objects.filter(id = request.POST['gid']).first()
        if group == None:
            return render(request,
                        pages['mySettings'],
                        {'you': you,
                        'message': "Error - The Group Could Not Be Edited."},
                        context_instance=RequestContext(request))

        group.displayname = request.POST['displayname']
        group.uname = request.POST['uname'].lower()
        group.desc = request.POST['desc']
        group.categories = request.POST['categories']

        group.save()

        if request.FILES:
            group = Groups.objects.filter(id = request.POST['gid']).first()

            aviFile = request.FILES['imageFileAvi']
            wpFile = request.FILES['imageFileWp']

            if not aviFile or \
            aviFile.name == '' or \
            not allowed_photo(aviFile.name):
                return render(request,
                            pages['mySettings'],
                            {'you': you,
                            'message': 'Error - Bad Avatar File Input...'},
                            context_instance=RequestContext(request))

            if not wpFile or \
            wpFile.name == '' or \
            not allowed_photo(wpFile.name):
                return render(request,
                            pages['mySettings'],
                            {'you': you,
                            'message': 'Error - Bad Wallpaper File Input...'},
                            context_instance=RequestContext(request))

            if aviFile and aviFile.name != '' and allowed_photo(aviFile.name):
                newdoc = AviModel(docfile = request.FILES['imageFileAvi'])
                newdoc.save()
                group.avi = newdoc.docfile.url

            if wpFile and wpFile.name != '' and allowed_photo(wpFile.name):
                newdoc = WpModel(docfile = request.FILES['imageFileWp'])
                newdoc.save()
                group.background = newdoc.docfile.url

            group.save()

            # print group
            # print group.serialize

        return render(request,
                    pages['mySettings'],
                    {'you': you, 'message': "Group Updated Successfully!"},
                    context_instance=RequestContext(request))


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)

def deleteGroup(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.filter(id = request.POST['gid']).first()

        if group != None:
            group.delete()
            return render(request,
                        pages['mySettings'],
                        {'you': you,
                        'message': "Group Deleted Successfully!"},
                        context_instance=RequestContext(request))

        else:
            return render(request,
                        pages['mySettings'],
                        {'you': you,
                        'message': "Error - Unable To Delete Group"},
                        context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def followUser(request, data):
    try:
        if data['user']['action'] != 'followUser':
            return JsonResponse({'msg': 'Error - Bad Action msg.'})

        you = Accounts.objects.get(uname = request.session['username'])
        user = Accounts.objects.get(uname = data['user']['uname'])

        print user.serialize

        if user == None:
            return JsonResponse({'msg': 'Error - User Could Not Be Loaded.'})

        checkFollow = Follows.objects \
        .filter(userid=you.id , follow_id=user.id).first()

        if checkFollow != None:
            return JsonResponse({'msg': 'Already Following.'})


        if user.status == 'public':
            newFollow = Follows(userid=you.id,
                                    user_rel=you,
                                    follow_id=user.id,
                                    follow_rel=user)
            newFollow.save()

            return JsonResponse({'msg': 'Now Following!',
                                'status': 'following'})

        if user.status == 'private':
            checkFollowRequest = FollowRequests.objects \
            .filter(sender_id=you.id , recipient_id=user.id).first()

            if checkFollowRequest != None:
                return JsonResponse({'msg': 'Follow Request Already Exist!'})

            if checkFollowRequest == None:
                newFollowRequest = FollowRequests(sender_id=you.id,
                                                    sender_rel=you,
                                                    recipient_id=user.id,
                                                    recipient_rel=user)
                newFollowRequest.save()

                return JsonResponse({'msg': 'Follow Request Sent!',
                                    'status': 'pending'})



    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def unfollowUser(request, data):
    try:
        if data['user']['action'] != 'unfollowUser':
            return JsonResponse({'msg': 'Error - Bad Action msg.'})

        you = Accounts.objects.get(uname = request.session['username'])
        user = Accounts.objects.get(uname = data['user']['uname'])

        if user == None:
            return JsonResponse({'msg': 'Error - User Could Not Be Loaded.'})

        checkFollow = Follows.objects \
        .filter(userid=you.id , follow_id=user.id).first()

        if checkFollow == None:
            return JsonResponse({'msg': 'Cannot Following.'})

        if checkFollow != None:
            checkFollow.delete()
            return JsonResponse({'msg': 'Unfollowed!',
                                'status': 'not following'})



    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def cancelPending(request, data):
    try:
        if data['user']['action'] != 'cancelPending':
            return JsonResponse({'msg': 'Error - Bad Action msg.'})

        you = Accounts.objects.get(uname = request.session['username'])
        user = Accounts.objects.get(uname = data['user']['uname'])

        if user == None:
            return JsonResponse({'msg': 'Error - User Could Not Be Loaded.'})

        checkFollowRequest = FollowRequests.objects \
        .filter(sender_id=you.id , recipient_id=user.id).first()

        if checkFollowRequest != None:
            checkFollowRequest.delete()
            return JsonResponse({'msg': 'Follow Request Canceled!',
                                'status': 'not following'})

        elif checkFollowRequest == None:
            return JsonResponse({'msg': 'Cannot Cancel Follow Request.'})



    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)
