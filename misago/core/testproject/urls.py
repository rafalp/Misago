from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^forum/', include('misago.urls')),
)

urlpatterns += patterns('misago.core.testproject.views',
    url(r'^forum/test-403/$', 'raise_misago_403', name='raise_misago_403'),
    url(r'^forum/test-404/$', 'raise_misago_404', name='raise_misago_404'),
    url(r'^test-403/$', 'raise_403', name='raise_403'),
    url(r'^test-404/$', 'raise_404', name='raise_404'),
)
