# --- --- --- --- #
# --- Imports --- #
# --- --- --- --- #

import bcrypt
import os, sys, cgi, random, string, hashlib, json, requests
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

import models
from models import Accounts, AviModel, WpModel, Groups, GroupMembers
from models import Follows, FollowRequests
from models import GroupRequests, GroupInvitations, Messages, MessageReply
from models import mediaPhotoModel, mediaVideoModel, mediaAudioModel
from models import Posts, Comments, Replies, Likes, Events, EventAttendees
from models import Conversations, ConvoMembers, ConvoMessages, ShareContent
from models import Products, Services, Transactions, Feedback

# from forms import PostForm

import routines
from routines import errorPage, genericPage, getYou

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
    try:
        request.session.flush()

        return redirect('/')

    except ValueError, KeyError:
        request.session.flush()

        return redirect('/')
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
def discoverView(request):
    if request.method == 'GET':
        if 'username' in request.session:
            you = getYou(request)
        else:
            you = None

        return render(request,
                        masterDICT['pages']['discoverView'],
                        {'error': "",
                        'you': you
                        },
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return None

# ---

@csrf_protect
def newestView(request):
    if request.method == 'GET':
        if 'username' in request.session:
            you = getYou(request)
        else:
            you = None

        posts = [z.serialize for z in Posts.objects.all().order_by('-date_created')[:10]]
        users = [z.serialize for z in Accounts.objects.all().order_by('-date_created')[:10]]
        groups = [z.serialize for z in Groups.objects.all().order_by('-date_created')[:10]]
        events = [z.serialize for z in Events.objects.all().order_by('-date_created')[:10]]
        products = [z.serialize for z in Products.objects.all().order_by('-date_created')[:10]]
        services = [z.serialize for z in Services.objects.all().order_by('-date_created')[:10]]

        # print posts, users, groups, events, products, services
        # print ' '

        return render(request,
                        masterDICT['pages']['newestView'],
                        {'error': "",
                        'you': you,
                        'posts': posts,
                        'users': users,
                        'groups': groups,
                        'events': events,
                        'products': products,
                        'services': services,
                        },
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return None

# ---

@csrf_protect
def featuredView(request):
    if request.method == 'GET':
        if 'username' in request.session:
            you = getYou(request)
        else:
            you = None

        posts = [z.serialize for z in Posts.objects.all().order_by('-date_created')[:10]]
        users = [z.serialize for z in Accounts.objects.all().order_by('-date_created')[:10]]
        groups = [z.serialize for z in Groups.objects.all().order_by('-date_created')[:10]]
        events = [z.serialize for z in Events.objects.all().order_by('-date_created')[:10]]
        products = [z.serialize for z in Products.objects.all().order_by('-date_created')[:10]]
        services = [z.serialize for z in Services.objects.all().order_by('-date_created')[:10]]

        # print posts, users, groups, events, products, services
        # print ' '

        return render(request,
                        masterDICT['pages']['featuredView'],
                        {'error': "",
                        'you': you,
                        'posts': posts,
                        'users': users,
                        'groups': groups,
                        'events': events,
                        'products': products,
                        'services': services,
                        },
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return None

# ---

@csrf_protect
def trendingView(request):
    if request.method == 'GET':
        if 'username' in request.session:
            you = getYou(request)
        else:
            you = None

        posts = [z.serialize for z in Posts.objects.all().order_by('-date_created')[:10]]
        users = [z.serialize for z in Accounts.objects.all().order_by('-date_created')[:10]]
        groups = [z.serialize for z in Groups.objects.all().order_by('-date_created')[:10]]
        events = [z.serialize for z in Events.objects.all().order_by('-date_created')[:10]]
        products = [z.serialize for z in Products.objects.all().order_by('-date_created')[:10]]
        services = [z.serialize for z in Services.objects.all().order_by('-date_created')[:10]]

        # print posts, users, groups, events, products, services
        # print ' '

        return render(request,
                        masterDICT['pages']['trendingView'],
                        {'error': "",
                        'you': you,
                        'posts': posts,
                        'users': users,
                        'groups': groups,
                        'events': events,
                        'products': products,
                        'services': services,
                        },
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return None

# ---

@csrf_protect
def productView(request, query):
    if request.method == 'GET':
        if 'username' in request.session:
            you = getYou(request)
        else:
            you = None

        product = Products.objects.filter(id = query).first()
        if product == None:
            msg = 'Product Not Found.'
            return errorPage(request, msg)

        product = product.serialize
        product['categories'] = '; '.join( product['categories'].split(';') )

        return render(request,
                        masterDICT['pages']['productView'],
                        {'error': "",
                        'you': you,
                        'product': product
                        },
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return None

# ---

@csrf_protect
def serviceView(request, query):
    if request.method == 'GET':
        if 'username' in request.session:
            you = getYou(request)
        else:
            you = None

        service = Services.objects.filter(id = query).first()
        if service == None:
            msg = 'Service Not Found.'
            return errorPage(request, msg)

        service = service.serialize
        service['categories'] = '; '.join( service['categories'].split(';') )

        return render(request,
                        masterDICT['pages']['serviceView'],
                        {'error': "",
                        'you': you,
                        'service': service
                        },
                        context_instance = RequestContext(request))

    if request.method == 'POST':
        return None

# ---

@csrf_protect
def dashboard(request):

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = getYou(request)
            following = Follows.objects.filter(userid=you.id)

            request.session['wall_id'] = you.id
            request.session['wall_type'] = masterDICT['ownerTypes']['account']

            # --- #

            feed = routines\
            .loadPostsA(id = you.id, you = you,
                        msg = masterDICT['fetchType']['posts']['main'])

            # --- #

            shareContents = ShareContent.objects \
            .filter(ownerid = you.id) \
            .order_by('-date_created')

            print '--- shareContents --- ', shareContents

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
            iu = []

            seeking = you.seeking.split(';')
            interests = you.interests.split(';')

            if seeking == ['']:
                seeking = []

            if interests == ['']:
                interests = []

            for s in seeking:
                users = Accounts.objects \
                .exclude(id = you.id).filter(seeking__contains=s)[:1]
                for u in users:
                    su.append( u.serialize )

            for i in interests:
                users = Accounts.objects \
                .exclude(id = you.id).filter(interests__contains=i)[:1]
                for u in users:
                    iu.append( u.serialize )

            su = su[:5]
            iu = iu[:5]

            # --- #

            return render(request, masterDICT['pages']['dashboard'],
                            {'you': you,
                            'posts': feed,
                            'suggestedGroups': suggestedGroups,
                            'similarSeeking': su,
                            'similarInterests': iu
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
            you = getYou(request)

            request.session['wall_id'] = you.id
            request.session['wall_type'] = masterDICT['ownerTypes']['account']

            followers = Follows.objects.filter(follow_id=you.id)
            following = Follows.objects.filter(userid=you.id)
            groups = GroupMembers.objects.filter(userid=you.id)

            posts = routines\
            .loadPostsA(id = you.id, you = you,
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
                you = getYou(request)
            else:
                you = None

            user = Accounts.objects \
            .filter( uname__iexact = query.lower() ).first()

            request.session['wall_id'] = user.id
            request.session['wall_type'] = masterDICT['ownerTypes']['account']

            if user == None:
                msg = 'User Account Not Found.'
                return errorPage(request, msg)


            followers = Follows.objects.filter(follow_id=user.id)
            following = Follows.objects.filter(userid=user.id)
            groups = GroupMembers.objects.filter(userid=user.id)

            if you != None:
                posts = routines \
                .loadPostsA(id = user.id, you = you, msg = masterDICT['fetchType']['posts']['user'])

            else:
                posts = routines \
                .loadPostsB(wall_id = user.id, wall_type = masterDICT['ownerTypes']['account'])

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
                                'groups': len(groups),
                                'posts': posts
                                },
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
                you = getYou(request)
            else:
                you = None

            group = Groups.objects \
            .filter(uname__iexact = query).first()

            request.session['wall_id'] = group.id
            request.session['wall_type'] = masterDICT['ownerTypes']['group']

            if group == None:
                msg = 'Group Not Found.'
                return errorPage(request, msg)


            if you != None:
                checkMembership = GroupMembers.objects \
                .filter(group_id = group.id, userid = you.id).first()

                if checkMembership != None or group.ownerid == you.id:
                    membership = 'yes'
                else:
                    membership = 'no'

            if you != None:
                posts = routines \
                .loadPostsA(id = group.id, you = you, msg = masterDICT['fetchType']['posts']['group'])

            else:
                membership = 'no'

                posts = routines \
                .loadPostsB(wall_id = group.id, wall_type = masterDICT['ownerTypes']['group'])

            return render(request,
                            masterDICT['pages']['GroupPage'],
                                {'you': you,
                                'group': group,
                                'posts': posts,
                                'membership': membership},
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
                you = getYou(request)
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
                                'post': post,
                                'posts': [post]},
                                context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)

# ---

@csrf_protect
def searchEngine(request):
    if request.method == 'GET':
        try:
            if 'username' in request.session:
                you = getYou(request)
            else:
                you = None


            return render(request,
                            masterDICT['pages']['searchEngine'],
                            {'you': you
                            },
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)


    if request.method == 'POST':
        data = json.loads(request.body)

        if data['action'] == 'search query':
            return routines.searchEngine(request, data)

        if data['action'] == 'searchUsers':
            return routines.searchUsers(request, data)

        if data['action'] == 'search for members':
            return routines.searchForMembers(request, data)

# ---

@csrf_protect
def searchResults(request, query):
    if request.method == 'GET':
        try:
            if 'username' in request.session:
                you = getYou(request)
            else:
                you = None

            info = routines.searchEngine(request, {'query': query})

            data = json.loads(str(info).replace("Content-Type: application/json", ""))

            posts = Posts.objects.filter(title__contains = query)[:10]
            posts = [p.serialize for p in posts]
            data['posts'] = posts
            dataJSON = json.dumps(data)

            return render(request,
                            masterDICT['pages']['searchView'],
                            {'you': you,
                            'dataJSON': dataJSON,
                            'users': data['users'],
                            'groups': data['groups'],
                            'events': data['events'],
                            'products': data['products'],
                            'services': data['services'],
                            'posts': data['posts'],
                            },
                            context_instance = RequestContext(request))

        except ObjectDoesNotExist:
            msg = 'User Account Not Found.'
            return errorPage(request, msg)


    if request.method == 'POST':
        return None

# ---

@csrf_protect
def messagesView(request):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = getYou(request)

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
            you = getYou(request)
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
            you = getYou(request)
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
            you = getYou(request)



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
def eventView(request, query):
    if request.method == 'POST':
        return redirect('/')

    if request.method == 'GET':
        if 'username' not in request.session:
            you = None
        else:
            you = getYou(request)

        event = Events.objects.filter(id = query).first()
        if event == None:
            msg = 'Event Not Found.'
            return errorPage(request, msg)

        event = event.serialize
        event['categories'] = ', '.join( event['categories'].split(' ') )

        return render(request,
                        masterDICT['pages']['eventview'],
                        {'you': you,
                        'event': event,
                        'message': ''},
                        context_instance = RequestContext(request))

# ---

@csrf_protect
def createView(request):

    if request.method == 'GET':
        if 'username' not in request.session:
            return redirect('/')

        try:
            you = getYou(request)
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

    if request.method != 'POST':
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

    if request.method != 'POST':
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

            if data['action'] == 'loadSettingsLists':
                return routines.loadSettingsLists(request)

        except:
            return JsonResponse({'msg': 'Failed To Load JSON Data...'})

    # ------------ #  # ------------ #  # ------------ #

# ---

@csrf_protect
def checkPoint(request):
    ''' This View Function Is Intended To Be Called By AJAX Requests Only '''
    if request.method != 'POST':
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

            if data['action'] == 'checkLoginState':
                return routines.checkLoginState(request, data)

        except KeyError:
            return JsonResponse({'msg': 'Failed To Load JSON Data...'})


# ---

@csrf_protect
def userActionFORM(request):
    ''' This View Function Is Intended To Be Called By Form Data Requests '''
    # if request.method != 'POST':
    #     return redirect('/')

    if request.method == 'POST':
        if request.POST['action'] == '' or request.POST['action'] == None:
            msg = 'Unknown Action...'
            return errorPage(request, msg)

        # --- #

        if request.POST['action'] == 'send message':
            return routines.sendMessage(request)

        if request.POST['action'] == 'sendGroupMessage':
            return routines.sendGroupMessage(request)

        if request.POST['action'] == 'createGroup':
            return routines.createGroup(request)

        if request.POST['action'] == 'createPost':
            return routines.createPost(request)

        if request.POST['action'] == 'createEvent':
            return routines.createEvent(request)

        if request.POST['action'] == 'createProduct':
            return routines.createProduct(request)

        if request.POST['action'] == 'createService':
            return routines.createService(request)


        else:
            msg = 'Unknown Action...'
            return errorPage(request, msg)

# ---


@csrf_protect
def userActionAJAX(request):
    ''' This View Function Is Intended To Be Called By AJAX Requests '''
    if request.method != 'POST':
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

            if data['action'] == 'shareContent':
                return routines.shareContent(request, data)

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
            you = getYou(request)
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
