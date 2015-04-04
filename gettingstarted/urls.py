from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reco/([0-9]+)', hello.views.ureco, name='reco'),
    url(r'^recov/(.*)', hello.views.vreco, name='recov'),
    url(r'^recot/([0-9]+)', hello.views.treco, name='recot'),

)
