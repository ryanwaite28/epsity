from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# ---



urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),

    url(r'^discover/$', views.discoverView, name='discoverview'),
    url(r'^newest/$', views.newestView, name='newestview'),
    url(r'^featured/$', views.featuredView, name='featuredview'),
    url(r'^trending/$', views.trendingView, name='trendingview'),
    url(r'^search/$', views.searchEngine, name='search'),
    url(r'^search/results/(?P<query>[a-zA-Z0-9\-\_]+)/$', views.searchResults, name='searchresults'),

    url(r'^error/$', views.errorPage, name='error_page'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^main/$', views.dashboard, name='dashboard'),
    url(r'^home/$', views.profileHome, name='profilehome'),

    url(r'^messages/$', views.messagesView, name='messagesview'),
    url(r'^conversations/$', views.conversationsView, name='conversationsView'),
    url(r'^create/$', views.createView, name='createview'),
    url(r'^mysettings/$', views.mySettings, name='mysettings'),
    url(r'^notifications/$', views.notificationsView, name='notifications'),
    url(r'^user/settingsaction/form/$', views.settingsActionFORM, name='settingsaction'),
    url(r'^user/settingsaction/ajax/$', views.settingsActionAJAX, name='settingsaction'),
    url(r'^checkpoint/$', views.checkPoint, name='checkpoint'),
    url(r'^action/form/$', views.userActionFORM, name='useractionform'),
    url(r'^action/ajax/$', views.userActionAJAX, name='useractionajax'),

    url(r'^events/$', views.eventsView, name='eventsview'),
    url(r'^events/(?P<query>[0-9]+)/$', views.eventView, name='eventview'),
    url(r'^products/(?P<query>[0-9]+)/$', views.productView, name='productview'),
    url(r'^services/(?P<query>[0-9]+)/$', views.serviceView, name='serviceview'),
    url(r'^users/(?P<query>[a-zA-Z0-9\-\_]+)/$', views.userPage, name='userpage'),
    #url(r'^users/(?P<query>[a-zA-Z0-9\-\_]+)/groupmember/$', views.userGroupMember, name='usergroupmember'),
    url(r'^groups/(?P<query>[a-zA-Z0-9\-\_]+)/$', views.groupPage, name='grouppage'),
    #url(r'^groups/(?P<query>[a-zA-Z0-9\-\_]+)/members/$', views.groupMembers, name='groupmembers'),
    url(r'^posts/(?P<query>[0-9]+)/$', views.postView, name='postview'),
    url(r'^eventsource/$', views.eventSource, name='eventsource'),

    url(r'^testing/$', views.testing, name='testing'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
