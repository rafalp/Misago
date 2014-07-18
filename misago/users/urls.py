from django.conf.urls import patterns, url


urlpatterns = patterns('misago.users.views.auth',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)


urlpatterns += patterns('misago.users.views.register',
    url(r'^register/$', 'register', name='register'),
    url(r'^register/completed/$', 'register_completed', name='register_completed'),
)


urlpatterns += patterns('misago.users.views.activation',
    url(r'^activation/request/$', 'request_activation', name="request_activation"),
    url(r'^activation/sent/$', 'activation_sent', name="activation_sent"),
    url(r'^activation/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activate_by_token', name="activate_by_token"),
)


urlpatterns += patterns('misago.users.views.forgottenpassword',
    url(r'^forgotten-password/$', 'request_reset', name='request_password_reset'),
    url(r'^forgotten-password/confirmation-sent/$', 'confirmation_sent', name='reset_password_confirmation_sent'),
    url(r'^forgotten-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'reset_password', name='reset_password_confirm'),
    url(r'^forgotten-password/password-sent/$', 'new_password_sent', name='request_password_new_sent'),
)


urlpatterns += patterns('misago.users.views.api',
    url(r'^api/validate/username/$', 'validate_username', name='api_validate_username'),
    url(r'^api/validate/username/(?P<user_id>\d+)/$', 'validate_username', name='api_validate_username'),
    url(r'^api/validate/email/$', 'validate_email', name='api_validate_email'),
    url(r'^api/validate/email/(?P<user_id>\d+)/$', 'validate_email', name='api_validate_email'),
    url(r'^api/validate/password/$', 'validate_password', name='api_validate_password'),
)


urlpatterns += patterns('misago.users.views.usercp',
    url(r'^usercp/forum-options/$', 'change_forum_options', name="usercp_change_forum_options"),
    url(r'^usercp/change-username/$', 'change_username', name="usercp_change_username"),
    url(r'^usercp/change-email-password/$', 'change_email_password', name="usercp_change_email_password"),
)
