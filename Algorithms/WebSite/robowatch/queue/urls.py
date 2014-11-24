from django.conf.urls import patterns, url

from queue import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #url(r'^(?P<pid>.+)/k$', views.search_k, name='search_k'),
    #url(r'^(?P<pid>.+)/s$', views.detail, name='detail'),
)

