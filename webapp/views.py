# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

import os, sys, cgi, random, string, hashlib, json
import webapp

from django.db.models import Q
from django.utils import timezone
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
from models import GroupRequests, GroupInvitations
from models import Posts, Comments, Replies, Likes, Events

# from forms import PostForm

import routines
from routines import errorPage, genericPage

from vaults import masterDICT
from vaults import webapp_dir, localPaths, serverPaths
from vaults import ALLOWED_AUDIO, ALLOWED_PHOTOS, ALLOWED_VIDEOS

# --- ----- --- #
# --- Views --- #
# --- ----- --- #

def welcome(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return redirect('/main/')
        else:
            return render(request, masterDICT['pages']['welcome'])


# ---

@csrf_protect
def login(request):
    if request.method == 'GET':
        if 'username' in request.session:
            return redirect('/home/')

        return render(request, masterDICT['pages']['login'], {'error': ''},
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return routines.loginAccount(request)

# ---

@csrf_protect
def logout(request):
    if request.method == 'POST':
        try:
            del request.session['username']
            del request.session['email']
            request.session.flush()

            return redirect('/')

        except KeyError:
            pass

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

        return render(request, masterDICT['pages']['signup'], {'error': ""},
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
            following = Follows.objects.filter(userid=you.id)

            # --- #

            feed = routines\
            .loadPosts(user_id = you.id, you = you,
                        msg = masterDICT['fetchType']['posts']['main'])

            # --- #

            suggestedGroups = []
            seeking = you.seeking.split(';')
            if seeking == ['']:
                seeking = []
            for s in seeking:
                groups = Groups.objects \
                .exclude(ownerid = you.id) \
                .filter(categories__contains = s)[:1]
                for g in groups:
                    suggestedGroups.append( g.serialize )
            suggestedGroups = suggestedGroups[:5]

            # --- #

            su = []
            interests = you.interests.split(';')
            if interests == ['']:
                interests = []
            for i in interests:
                users = Accounts.objects \
                .exclude(id = you.id) \
                .filter(interests__contains=i)[:1]
                for u in users:
                    su.append( u.serialize )
            su = su[:5]


            return render(request, masterDICT['pages']['profileMain'],
                            {'you': you,
                            'posts': feed,
                            'suggestedGroups': suggestedGroups,
                            'similar': su
                            },
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

            posts = routines\
            .loadPosts(user_id = you.id, you = you,
                        msg = masterDICT['fetchType']['posts']['home'])

            return render(request, masterDICT['pages']['profileHome'],
                            {'you': you,
                            'info': you.get_info,
                            'followers': len(followers),
                            'following': len(following),
                            'groups': len(groups),
                            'posts': posts
                            },
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

            posts = routines \
            .loadPosts(user_id = user.id, you = you, msg = '')

            if user == None:
                msg = 'User Account Not Found.'
                return errorPage(request, msg)

            else:
                if 'username' in request.session:
                    if user.uname == request.session['username']:
                        return redirect('/home')

                    else:
                        return render(request,
                                        masterDICT['pages']['UserPage'],
                                        {'you': you,
                                        'user': user,
                                        'info': user.get_info,
                                        'followers': len(followers),
                                        'following': len(following),
                                        'groups': len(groups),
                                        'posts': posts
                                        },
                                        context_instance = RequestContext(request))
                else:
                    return render(request,
                                    masterDICT['pages']['UserPage'],
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
                                masterDICT['pages']['GroupPage'],
                                {'you': you,
                                'group': group},
                                context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
def postView(request, query):
    if request.method == 'GET':
        # print query
        try:
            if 'username' in request.session:
                you = Accounts.objects.get(uname = request.session['username'])
                post = routines.loadPost_B(query, you)
            else:
                you = None
                post = routines.loadPost_A(query)

            if post == None:
                msg = 'Post Not Found.'
                return errorPage(request, msg)

            else:
                return render(request,
                                masterDICT['pages']['postView'],
                                {'you': you,
                                'post': post},
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
            return render(request, masterDICT['pages']['searchEngine'],
                            {'you': you},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)


    if request.method == 'POST':
        data = json.loads(request.body)

        if data['action'] == 'search query':
            return routines.searchEngine(request)

        if data['action'] == 'searchUsers':
            return routines.searchUsers(request)

        if data['action'] == 'search for members':
            return routines.searchForMembers(request)

# ---

@csrf_protect
def messagesView(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])

            return render(request, masterDICT['pages']['messagesView'],
                            {'you': you,
                            'message': '',
                            # 'messages': messages,
                            },
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
def conversationsView(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = Accounts.objects.get(uname = request.session['username'])
            return render(request, masterDICT['pages']['conversationsView'],
                            {'you': you,
                            'message': ''},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

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
            return render(request, masterDICT['pages']['mySettings'],
                            {'you': you,
                            'message': ''},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
def eventsView(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            you = None
        else:
            you = Accounts.objects.get(uname = request.session['username'])

        try:
            return render(request,
                            masterDICT['pages']['eventsview'],
                            {'you': you,
                            'message': ''},
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
            # post_form = PostForm()
            return render(request, masterDICT['pages']['createview'],
                            {'you': you,
                            'message': '',
                            # 'post_form': post_form
                            },
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

    # --- #

    if request.method == 'POST':
        msg = 'Unapproved Request Occurred...'
        return errorPage(request, msg)


# ---

@csrf_protect
def settingsActionFORM(request):
    ''' This View Is Intended To Be Used As A Form Handler '''

    if request.method == 'GET':
        return redirect('/mysettings')

    if request.method == 'POST':
        if request.POST['action'] == None or request.POST['action'] == '':
            return render(request, masterDICT['pages']['mySettings'],
                            {'you': you, 'message': 'Action Message Missing...'},
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
# ---

@csrf_protect
def settingsActionAJAX(request):
    ''' This View Is Intended To Be Used As An AJAX Handler '''

    if request.method == 'GET':
        return redirect('/mysettings')

    if request.method == 'POST':
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

        except:
            return JsonResponse({'msg': 'Failed To Load JSON Data...'})

    # ------------ #  # ------------ #  # ------------ #

# ---

@csrf_protect
def checkPoint(request):
    ''' This View Function Is Intended To Be Called By AJAX Requests Only '''
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if 'action' not in data:
                return JsonResponse({'msg': 'Action Message Is Missing...'})

            if data['action'] == None:
                return JsonResponse({'msg': 'Action Message Is Missing...'})

            if data['action'] == '':
                return JsonResponse({'msg': 'Action Message Is Empty/Unidentifiable...'})

            # ----- #

            if data['action'] == 'check group uname':
                return routines.checkGroupUserName(request, data)

            if data['action'] == 'checkConvoName':
                return routines.checkConvoName(request, data)

        except KeyError:
            return JsonResponse({'msg': 'Failed To Load JSON Data...'})


# ---

@csrf_protect
def userActionFORM(request):
    ''' This View Function Is Intended To Be Called By Form Data Requests '''
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        if request.POST['action'] == '' or request.POST['action'] == None:
            msg = 'Unknown Action...'
            return errorPage(request, msg)

        # --- #

        if request.POST['action'] == 'send message':
            return routines.sendMessage(request)

        if request.POST['action'] == 'sendGroupMessage':
            return routines.sendGroupMessage(request)

        if request.POST['action'] == 'create group':
            return routines.createGroup(request)

        if request.POST['action'] == 'create post':
            return routines.createUserPost(request)

        if request.POST['action'] == 'createEvent':
            return routines.createEvent(request)


        else:
            msg = 'Unknown Action...'
            return errorPage(request, msg)

# ---


@csrf_protect
def userActionAJAX(request):
    ''' This View Function Is Intended To Be Called By AJAX Requests '''
    if request.method == 'GET':
        return redirect('/')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print data
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

            if data['action'] == 'acceptFollow':
                return routines.acceptFollow(request, data)

            if data['action'] == 'declineFollow':
                return routines.declineFollow(request, data)

            # ---

            if data['action'] == 'sendGroupInvitation':
                return routines.sendGroupInvitation(request, data)

            if data['action'] == 'cancelPendingGroupInvite':
                return routines.cancelPendingGroupInvite(request, data)

            if data['action'] == 'removeMember':
                return routines.removeGroupMember(request, data)


            if data['action'] == 'acceptGroupInvite':
                return routines.acceptGroupInvite(request, data)

            if data['action'] == 'declineGroupInvite':
                return routines.declineGroupInvite(request, data)


            if data['action'] == 'acceptGroupRequest':
                return routines.acceptGroupRequest(request, data)

            if data['action'] == 'declineGroupRequest':
                return routines.declineGroupRequest(request, data)


            if data['action'] == 'leaveGroup':
                return routines.leaveGroup(request, data)

            if data['action'] == 'requestGroupInvite':
                return routines.requestGroupInvite(request, data)

            if data['action'] == 'cancelPendingGroupRequest':
                return routines.cancelPendingGroupRequest(request, data)

            # ---

            if data['action'] == 'load notes all':
                return routines.loadNotesAll(request, data)

            # ---

            if data['action'] == 'load messages':
                return routines.loadMessages(request)

            if data['action'] == 'loadMessageReplies':
                return routines.loadMessageReplies(request, data)

            if data['action'] == 'loadConversations':
                return routines.loadConversations(request, data)

            if data['action'] == 'getConversation':
                return routines.getConversation(request, data)

            if data['action'] == 'addPostCommentUser':
                return routines.addPostCommentUser(request, data)

            if data['action'] == 'addCommentReplyUser':
                return routines.addCommentReplyUser(request, data)

            if data['action'] == 'like':
                return routines.likeContent(request, data)

            if data['action'] == 'unlike':
                return routines.unlikeContent(request, data)

            # ---

            if data['action'] == 'createGroupConvo':
                return routines.createGroupConvo(request, data)


            else:
                msg = 'Unknown Action...'
                return errorPage(request, msg)

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
            return render(request, masterDICT['pages']['notificationsView'],
                            {'you': you, 'message': ''},
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)




# ---

def testing(request):
    if request.method == 'GET':
        if 'username' in request.session:
            you = Accounts.objects \
            .filter(uname = request.session['username']).first()
        else:
            you = None

        return render(request, masterDICT['pages']['testing'],
                        {'you': you, 'message': ''},
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        print [r for r in request.POST]

        if request.FILES:
            print '--- File(s) Detected ---'
            media = request.FILES['media']
            print media.name

        else:
            print '--- No File(s) Detected ---'


        test_html = render(request,
                                masterDICT['pages']['new_post'],
                                {'post': 'post'})
        test_html = str(test_html) \
        .replace("Content-Type: text/html; charset=utf-8" , "")


        return JsonResponse({'msg': 'admit-one', 'test_html': test_html})



def eventSource(request):
    return HttpResponse("Text only, please.", content_type="text/event-stream")


def pushNotif( obj ):
    return JsonResponse({'msg': 'admit-one'})
