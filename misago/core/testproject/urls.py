from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^forum/', include('misago.urls', namespace='misago')),
)

urlpatterns += patterns('misago.core.testproject.views',
    url(r'^forum/test-mail-user/$', 'test_mail_user', name='test_mail_user'),
    url(r'^forum/test-mail-users/$', 'test_mail_users', name='test_mail_users'),
    url(r'^forum/test-pagination/$', 'test_pagination', name='test_pagination'),
    url(r'^forum/test-pagination/(?P<page>[1-9][0-9]*)/$', 'test_pagination', name='test_pagination'),
    url(r'^forum/test-valid-slug/(?P<model_slug>[a-z0-9\-]+)-(?P<model_id>\d+)/$', 'validate_slug_view', name='validate_slug_view'),
    url(r'^forum/test-403/$', 'raise_misago_403', name='raise_misago_403'),
    url(r'^forum/test-404/$', 'raise_misago_404', name='raise_misago_404'),
    url(r'^test-403/$', 'raise_403', name='raise_403'),
    url(r'^test-404/$', 'raise_404', name='raise_404'),
)
