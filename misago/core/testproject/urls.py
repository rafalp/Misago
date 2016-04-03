from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^forum/', include('misago.urls', namespace='misago')),
)

urlpatterns += patterns('misago.core.testproject.views',
    url(r'^forum/test-mail-user/$', 'test_mail_user', name='test-mail-user'),
    url(r'^forum/test-mail-users/$', 'test_mail_users', name='test-mail-users'),
    url(r'^forum/test-pagination/$', 'test_pagination', name='test-pagination'),
    url(r'^forum/test-pagination/(?P<page>[1-9][0-9]*)/$', 'test_pagination', name='test-pagination'),
    url(r'^forum/test-valid-slug/(?P<slug>[a-z0-9\-]+)-(?P<pk>\d+)/$', 'validate_slug_view', name='validate-slug-view'),
    url(r'^forum/test-banned/$', 'raise_misago_banned', name='raise-misago-banned'),
    url(r'^forum/test-403/$', 'raise_misago_403', name='raise-misago-403'),
    url(r'^forum/test-404/$', 'raise_misago_404', name='raise-misago-404'),
    url(r'^forum/test-405/$', 'raise_misago_405', name='raise-misago-405'),
    url(r'^test-403/$', 'raise_403', name='raise-403'),
    url(r'^test-404/$', 'raise_404', name='raise-404'),
    url(r'^test-redirect/$', 'test_redirect', name='test-redirect'),
    url(r'^test-require-post/$', 'test_require_post', name='test-require-post'),
)
