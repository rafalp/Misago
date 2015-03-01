from django.conf.urls import patterns, url


urlpatterns = patterns('misago.users.api.auth',
    url(r'^auth/login/$', 'login', name='login'),
    url(r'^auth/$', 'user', name='auth_user'),
)


urlpatterns += patterns('misago.users.api.changepassword',
    url(r'^change-password/send-link/$', 'send_link', name='change_password_send_link'),
    url(r'^change-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/validate-token/$', 'validate_token', name='change_password_validate_token'),
    url(r'^change-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'change_password', name='change_password'),
)
