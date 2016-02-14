from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.core.views',
    url(r'^banned/$', 'home_redirect', name='banned')
)


urlpatterns += patterns('misago.users.views.auth',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)


urlpatterns += patterns('misago.users.views.activation',
    url(r'^request-activation/$', 'request_activation', name="request_activation"),
    url(r'^activation/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activate_by_token', name="activate_by_token"),
)


urlpatterns += patterns('misago.users.views.forgottenpassword',
    url(r'^forgotten-password/$', 'request_reset', name='forgotten_password'),
    url(r'^forgotten-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'reset_password_form', name='forgotten_password_change_form'),
)


urlpatterns += patterns('misago.users.views.options',
    url(r'^options/$', 'index', name='options'),
    url(r'^options/(?P<form_name>[-a-zA-Z]+)/$', 'index', name='options_form'),

    url(r'^options/forum-options/$', 'index', name='usercp_change_forum_options'),
    url(r'^options/change-username/$', 'index', name='usercp_change_username'),
    url(r'^options/sign-in-credentials/$', 'index', name='usercp_change_email_password'),

    url(r'^options/change-email/(?P<token>[a-zA-Z0-9]+)/$', 'confirm_email_change', name='options_confirm_email_change'),
    url(r'^options/change-password/(?P<token>[a-zA-Z0-9]+)/$', 'confirm_password_change', name='options_confirm_password_change'),
)


urlpatterns += patterns('',
    url(r'^users/', include(patterns('misago.users.views.lists',
        url(r'^$', 'lander', name="users"),
        url(r'^active-posters/$', 'active_posters', name="users_active_posters"),
        url(r'^(?P<rank_slug>[-a-zA-Z0-9]+)/$', 'rank', name="users_rank"),
        url(r'^(?P<rank_slug>[-a-zA-Z0-9]+)/(?P<page>\d+)/$', 'rank', name="users_rank"),
    )))
)


urlpatterns += patterns('',
    url(r'^user/(?P<user_slug>[a-zA-Z0-9]+)-(?P<user_id>\d+)/', include(patterns('misago.users.views.profile',
        url(r'^$', 'lander', name="user"),
        url(r'^posts/$', 'posts', name="user_posts"),
        url(r'^threads/$', 'threads', name="user_threads"),
        url(r'^followers/$', 'followers', name="user_followers"),
        url(r'^follows/$', 'follows', name="user_follows"),
        url(r'^username-history/$', 'username_history', name="username_history"),
        url(r'^ban-details/$', 'user_ban', name="user_ban"),
    )))
)


urlpatterns += patterns('',
    url(r'^user-avatar/', include(patterns('misago.users.views.avatarserver',
        url(r'^(?P<hash>[a-f0-9]+)/(?P<size>\d+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar', name="user_avatar"),
        url(r'^(?P<secret>[a-f0-9]+):(?P<hash>[a-f0-9]+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar_source', name="user_avatar_source"),
        url(r'^(?P<size>\d+)\.png$', 'serve_blank_avatar', name="blank_avatar"),
    )))
)
