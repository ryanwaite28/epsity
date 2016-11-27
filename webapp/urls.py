from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# ---



urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),

    url(r'^error/$', views.errorPage, name='error_page'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^main/$', views.profileMain, name='profilemain'),
    url(r'^home/$', views.profileHome, name='profilehome'),
    url(r'^search/$', views.searchEngine, name='search'),
    url(r'^create/$', views.createView, name='createview'),
    url(r'^mysettings/$', views.mySettings, name='mysettings'),
    url(r'^user/settingsaction/$', views.settingsAction, name='settingsaction'),
    url(r'^checkpoint/$', views.checkPoint, name='checkpoint'),
    url(r'^users/(?P<query>[a-zA-Z0-9]+)/$', views.searchUsers, name='searchusers'),
    url(r'^groups/(?P<query>[a-zA-Z0-9]+)/$', views.searchGroups, name='searchgroups'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
