from django.conf.urls import patterns, url

from recipe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^(?P<pid>.+)/o$', views.detail, name='detail'),
    #url(r'^(?P<pid>.+)/s$', views.detail, name='detail'),
    #url(r'^(?P<pid>.+).*/search/$', views.search, name='search'),
)
