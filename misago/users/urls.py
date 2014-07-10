from django.conf.urls import patterns, url


urlpatterns = patterns('misago.users.views.auth',
    url(r'^login/$', 'login', name='login'),
    url(r'^login/banned/$', 'login_banned', name='login_banned'),
    url(r'^logout/$', 'logout', name='logout'),
)


urlpatterns += patterns('misago.users.views.register',
    url(r'^register/$', 'register', name='register'),
    url(r'^register/completed/$', 'registration_completed', name='register_completed'),
)


urlpatterns += patterns('misago.users.views.api',
    url(r'^api/validate/username/$', 'validate_username', name='api_validate_username'),
    url(r'^api/validate/username/(?P<user_id>\d+)/$', 'validate_username', name='api_validate_username'),
    url(r'^api/validate/email/$', 'validate_email', name='api_validate_email'),
    url(r'^api/validate/email/(?P<user_id>\d+)/$', 'validate_email', name='api_validate_email'),
    url(r'^api/validate/password/$', 'validate_password', name='api_validate_password'),
)
