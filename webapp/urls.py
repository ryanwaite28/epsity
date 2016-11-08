from django.conf.urls import url, include
from . import views

# ---

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^main/$', views.profileMain, name='profilemain'),
    url(r'^home/$', views.profileHome, name='profilehome'),
]
