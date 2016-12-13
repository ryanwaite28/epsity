# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

import os, sys, cgi, random, string, hashlib, json
import datetime
import webapp

from django import forms
from django.utils import timezone
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
from models import GroupRequests, GroupInvitations, Messages, MessageReply
from models import mediaPhotoModel, mediaVideoModel, mediaAudioModel
from models import Posts, Comments, Replies, Likes

from vaults import ALLOWED_AUDIO, ALLOWED_PHOTOS, ALLOWED_VIDEOS, ALLOWED_MEDIA
from vaults import allowed_audio, allowed_photo, allowed_video, allowed_media
from vaults import masterDICT


# --- ----- ----- --- #
# --- Helper Code --- #
# --- ----- ----- --- #

def loadPosts(user_id, you, msg):
    if msg == None or msg == '':
        posts = Posts.objects \
        .filter( ownerid = user_id ) \
        .order_by('-date_created')[:10]

    elif msg == 'home':
        posts = Posts.objects \
        .filter( ownerid = you.id ) \
        .order_by('-date_created')[:10]

    elif msg == 'main':
        following = Follows.objects.filter(userid=you.id)
        posts = Posts.objects \
        .filter( Q( ownerid = you.id ) | Q(ownerid__in = [f.follow_id for f in following]) ) \
        .order_by('-date_created')[:10]

    else:
        posts = Posts.objects \
        .filter( ownerid = user_id ) \
        .order_by('-date_created')[:10]


    posts = [p.serialize for p in posts]
    for p in posts:
        p['content_type'] = masterDICT['contentTypes']['post']
        checkLike = Likes.objects \
        .filter(item_type=masterDICT['contentTypes']['post'],
                item_id=p['p_id'],
                owner_type=masterDICT['ownerTypes']['account'],
                ownerid=you.id).first()

        if checkLike != None:
            p['like_status'] = masterDICT['statuses']['like']['liked']
            p['like_status_json'] = json.dumps(masterDICT['statuses']['like']['liked'])

        else:
            p['like_status'] = masterDICT['statuses']['like']['not_liked']
            p['like_status_json'] = json.dumps(masterDICT['statuses']['like']['not_liked'])

        # ---

        likes = len( Likes.objects.filter \
        (item_type=masterDICT['contentTypes']['post'], item_id=p['p_id']) )
        p['likes'] = likes

        comments_len = len( Comments.objects.filter(post_id=p['p_id']) )
        p['comments_len'] = comments_len

        comments = Comments.objects \
        .filter(post_id=p['p_id']).order_by('date_created')[:5]

        comments = [c.serialize for c in comments]
        for c in comments:
            c['content_type'] = masterDICT['contentTypes']['comment']
            checkLike = Likes.objects \
            .filter(item_type=masterDICT['contentTypes']['comment'],
                    item_id=c['comment_id'],
                    owner_type=masterDICT['ownerTypes']['account'],
                    ownerid=you.id).first()

            if checkLike != None:
                c['like_status'] = masterDICT['statuses']['like']['liked']
                c['like_status_json'] = json.dumps(masterDICT['statuses']['like']['liked'])

            else:
                c['like_status'] = masterDICT['statuses']['like']['not_liked']
                c['like_status_json'] = json.dumps(masterDICT['statuses']['like']['not_liked'])

            # ---

            likes = len( Likes.objects \
            .filter(item_type=masterDICT['contentTypes']['comment'],
                    item_id=c['comment_id']) )

            c['likes'] = likes

            replies_len = len( Replies.objects \
            .filter(comment_id=c['comment_id']) )
            c['replies_len'] = replies_len

            replies = Replies.objects \
            .filter(comment_id=c['comment_id']) \
            .order_by('date_created')[:5]

            replies = [r.serialize for r in replies]
            for r in replies:
                r['content_type'] = masterDICT['contentTypes']['reply']
                checkLike = Likes.objects \
                .filter(item_type=masterDICT['contentTypes']['reply'],
                        item_id=r['reply_id'],
                        owner_type=masterDICT['ownerTypes']['account'],
                        ownerid=you.id).first()

                if checkLike != None:
                    r['like_status'] = masterDICT['statuses']['like']['liked']
                    r['like_status_json'] = json.dumps(masterDICT['statuses']['like']['liked'])

                else:
                    r['like_status'] = masterDICT['statuses']['like']['not_liked']
                    r['like_status_json'] = json.dumps(masterDICT['statuses']['like']['not_liked'])

                # ---

                likes = len( Likes.objects \
                .filter(item_type=masterDICT['contentTypes']['reply'],
                        item_id=r['reply_id']) )

                r['likes'] = likes


            c['replies'] = replies

        p['comments'] = comments


    return posts

# ---

def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)

# ---

def errorPage(request, msg = None):
    if msg == None or msg == '' or request.method == 'POST':
        # print '--- Error Page Redirecting...'
        return redirect('/')

    string = randomVal()
    return render(request,
                    masterDICT['pages']['error'],
                    {'errorMessage': msg,
                    'value': string})


def genericPage(request, msg, redirect):

    string = randomVal()
    return render(request,
                    masterDICT['pages']['generic'],
                    {'message': msg,
                    'redirect': redirect,
                    'value': string})

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
                            masterDICT['pages']['login'],
                            {'error': 'Incorrect Info.'},
                            context_instance=RequestContext(request))

        request.session['username'] = you.uname
        request.session['email'] = you.email

        you.last_active = datetime.datetime.now()
        you.save( update_fields=['last_active'] )

        return redirect('/home/')

    except ObjectDoesNotExist:
        return render(request,
                        masterDICT['pages']['login'],
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
                            masterDICT['pages']['signup'],
                            {'error': "That Email Is Already In Use."},
                            context_instance=RequestContext(request))

        checkUsername = Accounts.objects.filter(uname=uname).first()
        if checkUsername != None:
            return render(request,
                            masterDICT['pages']['signup'],
                            {'error': "That Username Is Already In Use."},
                            context_instance=RequestContext(request))

        newUser = Accounts(uname=uname.lower(),
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
                        masterDICT['pages']['signup'],
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
                    masterDICT['pages']['mySettings'],
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

        # print you.status

        return render(request,
                    masterDICT['pages']['mySettings'],
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
                    masterDICT['pages']['mySettings'],
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
                    masterDICT['pages']['mySettings'],
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
                        masterDICT['pages']['mySettings'],
                        {'you': you,
                        'message': "Avatar Updated Successfully!"},
                        context_instance=RequestContext(request))

        else:
            return render(request,
                        masterDICT['pages']['mySettings'],
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
                        masterDICT['pages']['mySettings'],
                        {'you': you,
                        'message': "Wallpaper Updated Successfully!"},
                        context_instance=RequestContext(request))

        else:
            return render(request,
                        masterDICT['pages']['mySettings'],
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
    .filter(uname__contains = data['query'])[:25]
    groups = Groups.objects \
    .exclude(ownerid = you.id) \
    .filter(uname__contains = data['query'])[:25]

    users = [u.serialize for u in users]
    groups = [g.serialize for g in groups]

    for u in users:
        checkFollow = Follows.objects \
        .filter(userid = you.id, follow_id = u['userid']).first()

        if checkFollow == None:
            checkFollowRequest = FollowRequests.objects \
            .filter(sender_id=you.id , recipient_id=u['userid']).first()

            if checkFollowRequest != None:
                u['status'] = masterDICT['followStates']['pending']['status']
                u['btn'] = masterDICT['followStates']['pending']['btn']
                u['msg'] = masterDICT['followStates']['pending']['msg']
                u['action'] = masterDICT['followStates']['pending']['action']
                u['title'] = masterDICT['followStates']['pending']['title']

            else:
                u['status'] = masterDICT['followStates']['not_following']['status']
                u['btn'] = masterDICT['followStates']['not_following']['btn']
                u['msg'] = masterDICT['followStates']['not_following']['msg']
                u['action'] = masterDICT['followStates']['not_following']['action']
                u['title'] = masterDICT['followStates']['not_following']['title']

        if checkFollow != None:
            u['status'] = masterDICT['followStates']['following']['status']
            u['btn'] = masterDICT['followStates']['following']['btn']
            u['msg'] = masterDICT['followStates']['following']['msg']
            u['action'] = masterDICT['followStates']['following']['action']
            u['title'] = masterDICT['followStates']['following']['title']

    # print users

    for g in groups:
        checkMembership = GroupMembers.objects \
        .filter(group_id = g['gid'], userid = you.id).first()

        if checkMembership == None:
            checkGroupRequests = GroupRequests.objects \
            .filter(group_id=g['gid'], userid=you.id).first()

            if checkGroupRequests != None:
                g['status'] = masterDICT['groupStates']['user']['pending']['status']
                g['btn'] = masterDICT['groupStates']['user']['pending']['btn']
                g['msg'] = masterDICT['groupStates']['user']['pending']['msg']
                g['action'] = masterDICT['groupStates']['user']['pending']['action']
                g['title'] = masterDICT['groupStates']['user']['pending']['title']

            else:
                g['status'] = masterDICT['groupStates']['user']['not_member']['status']
                g['btn'] = masterDICT['groupStates']['user']['not_member']['btn']
                g['msg'] = masterDICT['groupStates']['user']['not_member']['msg']
                g['action'] = masterDICT['groupStates']['user']['not_member']['action']
                g['title'] = masterDICT['groupStates']['user']['not_member']['title']

        else:
            g['status'] = masterDICT['groupStates']['user']['member']['status']
            g['btn'] = masterDICT['groupStates']['user']['member']['btn']
            g['msg'] = masterDICT['groupStates']['user']['member']['msg']
            g['action'] = masterDICT['groupStates']['user']['member']['action']
            g['title'] = masterDICT['groupStates']['user']['member']['title']

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

    if 'limit' in data:
        if data['limit'] == None or data['limit'] == '' or data['limit'] >= 30:
            data['limit'] = 30
    else:
        data['limit'] = 30

    users = Accounts.objects \
    .exclude(id = you.id) \
    .filter(uname__contains = data['query'])[:data['limit']]

    users = [u.serialize for u in users]

    for u in users:
        checkMembership = GroupMembers.objects \
        .filter(group_id = data['gid'], userid = u['userid']).first()

        if checkMembership == None:
            checkGroupInvite = GroupInvitations.objects \
            .filter(group_id=data['gid'], userid=u['userid']).first()

            if checkGroupInvite != None:
                u['status'] = masterDICT['groupStates']['owner']['pending']['status']
                u['btn'] = masterDICT['groupStates']['owner']['pending']['btn']
                u['msg'] = masterDICT['groupStates']['owner']['pending']['msg']
                u['action'] = masterDICT['groupStates']['owner']['pending']['action']
                u['title'] = masterDICT['groupStates']['owner']['pending']['title']

            else:
                u['status'] = masterDICT['groupStates']['owner']['not_member']['status']
                u['btn'] = masterDICT['groupStates']['owner']['not_member']['btn']
                u['msg'] = masterDICT['groupStates']['owner']['not_member']['msg']
                u['action'] = masterDICT['groupStates']['owner']['not_member']['action']
                u['title'] = masterDICT['groupStates']['owner']['not_member']['title']

        else:
            u['status'] = masterDICT['groupStates']['owner']['member']['status']
            u['btn'] = masterDICT['groupStates']['owner']['member']['btn']
            u['msg'] = masterDICT['groupStates']['owner']['member']['msg']
            u['action'] = masterDICT['groupStates']['owner']['member']['action']
            u['title'] = masterDICT['groupStates']['owner']['member']['title']

    # print users

    resp = {
        'msg': 'search results',
        'users': users,
    }

    return JsonResponse(resp)

# ---

def searchUsers(request):
    data = json.loads(request.body)
    you = Accounts.objects.get(uname = request.session['username'])

    if data['query'] == None:
        return JsonResponse({'msg': 'Query Is Missing...'})

    if data['query'] == '':
        return JsonResponse({'msg': 'Query Is Empty/Unidentifiable...'})

    if 'limit' in data:
        if data['limit'] == None or data['limit'] == '' or data['limit'] >= 30:
            data['limit'] = 30
    else:
        data['limit'] = 30

    users = Accounts.objects \
    .exclude(id = you.id) \
    .filter(uname__contains = data['query'])[:data['limit']]

    users = [u.serialize for u in users]

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
                        masterDICT['pages']['createview'],
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
                            masterDICT['pages']['createview'],
                            {'you': you,
                            'message': 'Error - Bad Avatar File Input...'},
                            context_instance=RequestContext(request))

            if not wpFile or \
            wpFile.name == '' or \
            not allowed_photo(wpFile.name):
                return render(request,
                            masterDICT['pages']['createview'],
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

        # return render(request,
        #             masterDICT['pages']['createview'],
        #             {'you': you, 'message': "New Group Created!"},
        #             context_instance=RequestContext(request))

        return genericPage(request = request,
                            msg = 'Group Created!',
                            redirect=request.POST['origin'])


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
                        masterDICT['pages']['mySettings'],
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
                            masterDICT['pages']['mySettings'],
                            {'you': you,
                            'message': 'Error - Bad Avatar File Input...'},
                            context_instance=RequestContext(request))

            if not wpFile or \
            wpFile.name == '' or \
            not allowed_photo(wpFile.name):
                return render(request,
                            masterDICT['pages']['mySettings'],
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
                    masterDICT['pages']['mySettings'],
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
                        masterDICT['pages']['mySettings'],
                        {'you': you,
                        'message': "Group Deleted Successfully!"},
                        context_instance=RequestContext(request))

        else:
            return render(request,
                        masterDICT['pages']['mySettings'],
                        {'you': you,
                        'message': "Error - Unable To Delete Group"},
                        context_instance=RequestContext(request))

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


# ------- #

def followUser(request, data):
    try:
        if data['user']['action'] != 'followUser':
            return JsonResponse({'msg': 'Error - Bad Action msg.'})

        you = Accounts.objects.get(uname = request.session['username'])
        user = Accounts.objects.get(uname = data['user']['uname'])

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
                                    'status': 'following',
                                    'state': masterDICT['followStates']['following']})

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
                                        'status': 'pending',
                                        'state': masterDICT['followStates']['pending']})



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
                                'status': 'not following',
                                'state': masterDICT['followStates']['not_following']})



    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def cancelPendingFollow(request, data):
    try:
        if data['user']['action'] != 'cancelPendingFollow':
            return JsonResponse({'msg': 'Error - Bad Action msg.'})

        you = Accounts.objects.get(uname = request.session['username'])
        user = Accounts.objects.filter(uname = data['user']['uname']).first()

        if user == None:
            return JsonResponse({'msg': 'Error - User Could Not Be Loaded.'})

        checkFollowRequest = FollowRequests.objects \
        .filter(sender_id=you.id , recipient_id=user.id).first()

        if checkFollowRequest != None:
            checkFollowRequest.delete()
            return JsonResponse({'msg': 'Follow Request Canceled!',
                                'status': 'not following',
                                'state': masterDICT['followStates']['not_following']})

        elif checkFollowRequest == None:
            return JsonResponse({'msg': 'Cannot Cancel Follow Request.'})



    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)

# ------- #

def loadNotesAll(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])

        pendingFollows = FollowRequests.objects.filter(recipient_id = you.id)
        pendingFollows = [pf.serialize for pf in pendingFollows]
        for pf in pendingFollows:
            # pf['status'] = masterDICT['followStates']['pending']['status']
            # pf['btn'] = masterDICT['followStates']['pending']['btn']
            # pf['msg'] = masterDICT['followStates']['pending']['msg']
            # pf['action'] = masterDICT['followStates']['pending']['action']
            # pf['title'] = masterDICT['followStates']['pending']['title']
            pf['options'] = masterDICT['followStates']['options']


        pendingGroupInvites = GroupInvitations.objects.filter(userid = you.id)
        pendingGroupInvites = [pi.serialize for pi in pendingGroupInvites]
        for pi in pendingGroupInvites:
            # pi['status'] = masterDICT['groupStates']['user']['pending']['status']
            # pi['btn'] = masterDICT['groupStates']['user']['pending']['btn']
            # pi['msg'] = masterDICT['groupStates']['user']['pending']['msg']
            # pi['action'] = masterDICT['groupStates']['user']['pending']['action']
            # pi['title'] = masterDICT['groupStates']['user']['pending']['title']
            pi['options'] = masterDICT['groupStates']['user']['options']


        pendingGroupRequests = []

        groups = Groups.objects.filter(ownerid =  you.id)
        groups = [g.serialize for g in groups]
        for g in groups:
            pendingRequests = GroupRequests.objects.filter(group_id = g['gid'])
            pendingRequests = [pr.serialize for pr in pendingRequests]
            for pr in pendingRequests:
                # pr['status'] = masterDICT['groupStates']['owner']['pending']['status']
                # pr['btn'] = masterDICT['groupStates']['owner']['pending']['btn']
                # pr['msg'] = masterDICT['groupStates']['owner']['pending']['msg']
                # pr['action'] = masterDICT['groupStates']['owner']['pending']['action']
                # pr['title'] = masterDICT['groupStates']['owner']['pending']['title']
                pr['options'] = masterDICT['groupStates']['owner']['options']

                pendingGroupRequests.append(pr)


        resp = {
            'msg': 'Notes All',
            'pendingFollows': pendingFollows,
            'pendingGroupInvites': pendingGroupInvites,
            'pendingGroupRequests': pendingGroupRequests
        }

        return JsonResponse(resp)

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def acceptFollow(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        if you.id != data['pf']['recipient_rel']['userid']:
            return JsonResponse({'msg': 'Error - Conflict Occured.'})

        pendingFollow = FollowRequests.objects \
        .filter(sender_id = data['pf']['sender_rel']['userid'],
            recipient_id = data['pf']['recipient_rel']['userid']).first()

        if pendingFollow == None:
            return JsonResponse({'msg': 'Error - Conflict Occured.'})

        else:
            user = Accounts.objects \
            .get(uname = data['pf']['sender_rel']['uname'])

            newFollow = Follows(userid=user.id,
                                    user_rel=user,
                                    follow_id=you.id,
                                    follow_rel=you)
            newFollow.save()
            pendingFollow.delete()

            return JsonResponse({'msg': 'Follow Accepted!'})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



def declineFollow(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        if you.id != data['pf']['recipient_rel']['userid']:
            return JsonResponse({'msg': 'Error - Conflict Occured.'})

        pendingFollow = FollowRequests.objects \
        .filter(sender_id = data['pf']['sender_rel']['userid'],
            recipient_id = data['pf']['recipient_rel']['userid']).first()

        if pendingFollow == None:
            return JsonResponse({'msg': 'Error - Conflict Occured.'})

        else:
            pendingFollow.delete()

            return JsonResponse({'msg': 'Follow Declined!'})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


# ------- #


def sendGroupInvitation(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.filter(id =  data['group']['gid']).first()

        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkMembership = GroupMembers.objects.filter \
        (group_id = data['group']['gid'], userid = data['user']['userid']).first()

        if checkMembership != None:
            return JsonResponse({'msg': 'Already A Member'})

        if checkMembership == None:
            checkGroupInvite = GroupInvitations.objects.filter \
            (group_id=data['group']['gid'], userid=data['user']['userid']).first()

            if checkGroupInvite != None:
                return JsonResponse({'msg': 'Already A Pending Invite'})

            if checkGroupInvite == None:
                user = Accounts.objects.get(id = data['user']['userid'])

                newGroupInvite = GroupInvitations \
                (group_id = group.id, group_rel = group,
                userid = user.id, user_rel = user)

                newGroupInvite.save()

                return JsonResponse({'msg': 'Group Invite Created!',
                                    'status': 'pending',
                                    'state': masterDICT['groupStates']['user']['pending']})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



def requestGroupInvite(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.filter(id =  data['group']['gid']).first()

        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkMembership = GroupMembers.objects.filter \
        (group_id = group.id, userid = you.id).first()

        if checkMembership != None:
            return JsonResponse({'msg': 'Already A Member'})

        if checkMembership == None:
            checkGroupRequest = GroupRequests.objects.filter \
            (group_id = group.id, userid = you.id).first()

            if checkGroupRequest != None:
                return JsonResponse({'msg': 'Already A Pending Invite'})

            if checkGroupRequest == None:
                newGroupRequest = GroupRequests \
                (group_id = group.id, group_rel = group,
                userid = you.id, user_rel = you)

                newGroupRequest.save()

                return JsonResponse({'msg': 'Group Invite Created!',
                                    'status': 'pending',
                                    'state': masterDICT['groupStates']['user']['pending']})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def acceptGroupInvite(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.get(id =  data['pi']['group_rel']['gid'])
        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkGroupInvite = GroupInvitations.objects.filter \
        (group_id=group.id, userid=data['pi']['userid']).first()

        if checkGroupInvite == None:
            return JsonResponse({'msg': 'Group Invite Not Found!'})

        if checkGroupInvite != None:

            user = Accounts.objects.filter(id = data['pi']['userid']).first()

            newGroupMember = GroupMembers \
            (group_id = group.id, group_rel = group,
            userid = user.id, user_rel = user)

            newGroupMember.save()
            checkGroupInvite.delete()

            return JsonResponse({'msg': 'Group Invite Accepted!',
                                'status': 'currently a member'})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def declineGroupInvite(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.get(id =  data['pi']['group_rel']['gid'])
        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkGroupInvite = GroupInvitations.objects.filter \
        (group_id=group.id, userid=data['pi']['userid']).first()

        if checkGroupInvite == None:
            return JsonResponse({'msg': 'Group Invite Not Found!'})

        if checkGroupInvite != None:
            checkGroupInvite.delete()
            return JsonResponse({'msg': 'Group Invite Declined!',
                                'status': 'not a member'})


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def acceptGroupRequest(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.filter(id =  data['pr']['group_rel']['gid']).first()

        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkGroupRequest = GroupRequests.objects.filter \
        (group_id=group.id, userid=data['pr']['userid']).first()

        if checkGroupRequest == None:
            return JsonResponse({'msg': 'Group Invite Not Found!'})

        if checkGroupRequest != None:

            user = Accounts.objects.filter(id = data['pr']['userid']).first()

            newGroupMember = GroupMembers \
            (group_id = group.id, group_rel = group,
            userid = user.id, user_rel = user)

            newGroupMember.save()
            checkGroupRequest.delete()

            return JsonResponse({'msg': 'Group Request Accepted!',
                                'status': 'currently a member'})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def declineGroupRequests(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.filter(id =  data['pr']['group_rel']['gid']).first()

        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkGroupInvite = GroupRequests.objects.filter \
        (group_id=group.id, userid=data['pr']['userid']).first()

        if checkGroupInvite == None:
            return JsonResponse({'msg': 'Group Invite Not Found!'})

        if checkGroupInvite != None:
            checkGroupInvite.delete()
            return JsonResponse({'msg': 'Group Invite Declined!',
                                'status': 'not a member'})


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def cancelPendingGroupInvite(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.get(id =  data['group']['gid'])

        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkGroupInvite = GroupInvitations.objects.filter \
        (group_id=data['group']['gid'], userid = data['user']['userid']).first()

        if checkGroupInvite == None:
            return JsonResponse({'msg': 'Error - Group Invite Not Found'})

        if checkGroupInvite != None:
            checkGroupInvite.delete()

            return JsonResponse({'msg': 'Group Invite Canceled!',
                                'status': 'not a member',
                                'state': masterDICT['groupStates']['owner']['not_member']})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



def cancelPendingGroupRequest(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.filter(id =  data['group']['gid']).first()

        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkGroupRequest = GroupRequests.objects.filter \
        (group_id = group.id, userid = you.id).first()

        if checkGroupRequest == None:
            return JsonResponse({'msg': 'Error - Group Request Not Found'})

        if checkGroupRequest != None:
            checkGroupRequest.delete()

            return JsonResponse({'msg': 'Group Request Canceled!',
                                'status': 'not a member',
                                'state': masterDICT['groupStates']['user']['not_member']})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



def removeGroupMember(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.get(id =  data['group']['gid'])
        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkMembership = GroupMembers.objects.filter \
        (group_id = data['group']['gid'], userid = data['user']['userid']).first()

        if checkMembership == None:
            return JsonResponse({'msg': 'User Is Not A Member'})

        if checkMembership != None:
            checkMembership.delete()
            return JsonResponse({'msg': 'Group Invite Created!',
                                'status': 'not a member'})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def leaveGroup(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        group = Groups.objects.filter(id =  data['group']['gid']).first()

        if group == None:
            return JsonResponse({'msg': 'Error - Group Cannot Be Loaded.'})

        checkMembership = GroupMembers.objects.filter \
        (group_id = group.id, userid = you.id).first()

        if checkMembership == None:
            return JsonResponse({'msg': 'User Is Not A Member'})

        if checkMembership != None:
            checkMembership.delete()
            return JsonResponse({'msg': 'left group',
                                'status': 'not a member',
                                'state': masterDICT['groupStates']['user']['not_member']})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def loadMessages(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])

        messages = Messages.objects \
        .filter( Q(userA_id = you.id) | Q(userB_id = you.id) )

        messages = [m.serialize for m in messages]
        for m in messages:
            messageReplies = MessageReply.objects \
            .filter( message_id = m['mid'] )

            messagesReplies = [mr.serialize for mr in messageReplies]
            for mr in messagesReplies:
                if mr['userid'] == you.id:
                    mr['pos'] = 'right'
                    mr['color'] = 'lightgrey'

                else:
                    mr['pos'] = 'left'
                    mr['color'] = '#fbfbfb'

                if mr['attachment'] != '':
                    mr['class'] = 'transition btn btn-sm btn-default point-cursor'

                else:
                    mr['class'] = 'transition point-cursor'

            m['replies'] = messagesReplies

        resp = {
            'msg': 'loaded messaged',
            'you': you.serialize,
            'messages': messages
        }

        # print resp

        return JsonResponse(resp)

    except ObjectDoesNotExist:
        msg = 'Server Side Error Occured.'
        return errorPage(request, msg)


def sendMessage(request):
    try:
        sender = Accounts.objects \
        .filter(id = request.POST['senderid']).first() # You

        recipient = Accounts.objects \
        .filter(id = request.POST['recipientid']).first() # Recipient

        if sender == None or recipient == None:
            msg = 'Error - A User Account Could Not Be Found.'
            return errorPage(request, msg)

        # ---

        existingMessages = Messages.objects \
        .filter( Q(userA_id = sender.id) | Q(userB_id = sender.id) ) \
        .filter( Q(userA_id = recipient.id) | Q(userB_id = recipient.id) ) \
        .first()

        # ---

        newdoc = None # Default For Message Media
        doctype = ''

        if request.FILES:
            media = request.FILES['media']

            if media and media.name != '':
                if allowed_audio(media.name):
                    newdoc = mediaAudioModel(docfile = request.FILES['media'])
                    doctype = 'Audio'

                elif allowed_video(media.name):
                    newdoc = mediaVideoModel(docfile = request.FILES['media'])
                    doctype = 'Video'

                elif allowed_photo(media.name):
                    newdoc = mediaPhotoModel(docfile = request.FILES['media'])
                    doctype = 'Photo'

                else:
                    return genericPage(request = request,
                                        msg = 'Error - Bad Media File Input.',
                                        redirect=request.POST['origin'])


                newdoc.save()

            else:
                return genericPage(request = request,
                                    msg = 'Error - Bad Media File Input.',
                                    redirect=request.POST['origin'])

        # ---

        if existingMessages != None:
            newMessageReply = MessageReply(message_id=existingMessages.id,
                                            message_rel=existingMessages,
                                            userid=sender.id,
                                            user_rel=sender,
                                            contents=cgi.escape(request.POST['contents']))

        if existingMessages == None:
            newMessages = Messages(userA_id=sender.id,
                                    userA_rel=sender,
                                    userB_id=recipient.id,
                                    userB_rel=recipient)

            newMessages.save()

            newMessageReply = MessageReply(message_id=newMessages.id,
                                            message_rel=newMessages,
                                            userid=sender.id,
                                            user_rel=sender,
                                            contents=cgi.escape(request.POST['contents']))
        # ---

        if newdoc != None:
            newMessageReply.attachment = newdoc.docfile.url

        if doctype != '':
            newMessageReply.attachment_type = doctype

        newMessageReply.save()

        return genericPage(request = request,
                            msg = 'Message Sent!',
                            redirect=request.POST['origin'])

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



def createUserPost(request):
    try:
        you = Accounts.objects.get(uname = request.session['username'])

        # ----- #

        newdoc = None # Default For Message Media
        doctype = ''

        if request.FILES:
            media = request.FILES['media']

            if media and media.name != '':
                if allowed_audio(media.name):
                    newdoc = mediaAudioModel(docfile = request.FILES['media'])
                    doctype = 'Audio'

                elif allowed_video(media.name):
                    newdoc = mediaVideoModel(docfile = request.FILES['media'])
                    doctype = 'Video'

                elif allowed_photo(media.name):
                    newdoc = mediaPhotoModel(docfile = request.FILES['media'])
                    doctype = 'Photo'

                else:
                    return genericPage(request = request,
                                        msg = 'Error - Bad Media File Input.',
                                        redirect=request.POST['origin'])

                newdoc.save()

            else:
                return genericPage(request = request,
                                    msg = 'Error - Bad Media File Input.',
                                    redirect=request.POST['origin'])

        # ----- #

        newPost = Posts(ownerid = you.id,
                        owner_type = masterDICT['ownerTypes']['account'],
                        title = cgi.escape(request.POST['title']),
                        contents = cgi.escape(request.POST['contents']),
                        link = request.POST['link'],
                        post_type = request.POST['post_type'])

        if newdoc != None:
            newPost.attachment = newdoc.docfile.url

        if doctype != '':
            newPost.attachment_type = doctype

        newPost.save()

        return genericPage(request = request,
                            msg = 'Post Created!',
                            redirect=request.POST['origin'])


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



def addPostCommentUser(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        post = Posts.objects.filter(id =  data['info']['post_id']).first()

        if post == None:
            return JsonResponse({'msg': 'Error - Post Cannot Be Loaded.'})

        newComment = Comments(ownerid = you.id,
                                owner_type = masterDICT['ownerTypes']['account'],
                                post_id = post.id,
                                post_rel = post,
                                contents = cgi.escape(data['info']['comment']))

        newComment.save()

        comment = newComment.serialize
        comment['content_type'] = masterDICT['contentTypes']['comment']
        comment['like_status'] = masterDICT['statuses']['like']['not_liked']
        comment['like_status_json'] = json.dumps(masterDICT['statuses']['like']['not_liked'])

        comment_html = render(request,
                                masterDICT['pages']['new_comment'],
                                {'comment': comment})

        comment_html = str(comment_html) \
        .replace("Content-Type: text/html; charset=utf-8" , "")

        commentMeter = int(data['info']['comments']) + 1

        return JsonResponse({'msg': 'comment added',
                                'comment': newComment.serialize,
                                'comment_html': comment_html,
                                'commentMeter': commentMeter})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)



def addCommentReplyUser(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        comment = Comments.objects.filter(id =  data['info']['comment_id']).first()

        if comment == None:
            return JsonResponse({'msg': 'Error - Comment Cannot Be Loaded.'})

        newReply = Replies(ownerid = you.id,
                            owner_type = masterDICT['ownerTypes']['account'],
                            comment_id = comment.id,
                            comment_rel = comment,
                            contents = cgi.escape(data['info']['reply']))

        newReply.save()

        reply = newReply.serialize
        reply['content_type'] = masterDICT['contentTypes']['reply']
        reply['like_status'] = masterDICT['statuses']['like']['not_liked']
        reply['like_status_json'] = json.dumps(masterDICT['statuses']['like']['not_liked'])

        reply_html = render(request,
                                masterDICT['pages']['new_reply'],
                                {'reply': reply})

        reply_html = str(reply_html) \
        .replace("Content-Type: text/html; charset=utf-8" , "")

        replyMeter = int(data['info']['replies']) + 1

        return JsonResponse({'msg': 'reply added',
                                'reply': newReply.serialize,
                                'reply_html': reply_html,
                                'replyMeter': replyMeter})

    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def likeContent(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        likeMeter = int(data['info']['likes'])

        newLike = Likes(ownerid = you.id,
                        owner_type = masterDICT['ownerTypes']['account'],
                        item_id = data['info']['contentID'],
                        item_type = data['info']['contentType'])

        newLike.save()

        likeMeter += 1

        return JsonResponse \
        ({'msg': 'content liked',
        'likeMeter': likeMeter,
        'likeStatus': masterDICT['statuses']['like']['liked']})


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)


def unlikeContent(request, data):
    try:
        you = Accounts.objects.get(uname = request.session['username'])
        likeMeter = int(data['info']['likes'])

        like = Likes.objects \
        .filter(ownerid = you.id,
                    owner_type = masterDICT['ownerTypes']['account'],
                    item_id = data['info']['contentID'],
                    item_type = data['info']['contentType'])

        if like == None:
            return JsonResponse({'msg': 'Error - Cannot Load Like'})

        like.delete()

        likeMeter -= 1

        return JsonResponse \
        ({'msg': 'content unliked',
            'likeMeter': likeMeter,
            'likeStatus': masterDICT['statuses']['like']['not_liked']})


    except ObjectDoesNotExist:
        msg = 'User Account Not Found.'
        return errorPage(request, msg)
