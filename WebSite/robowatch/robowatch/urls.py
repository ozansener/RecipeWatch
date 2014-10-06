from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'robowatch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^search/',include('search.urls',namespace="search")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^q/',include('queue.urls')),
)
