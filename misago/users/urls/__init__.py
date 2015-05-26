from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.users.views.auth',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)


urlpatterns += patterns('misago.users.views.activation',
    url(r'^activation/$', 'activation_noscript', name="request_activation"),
    url(r'^activation/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activation_noscript', name="activate_by_token"),
)


urlpatterns += patterns('misago.users.views.forgottenpassword',
    url(r'^forgotten-password/$', 'forgotten_password_noscript', name='forgotten_password'),
    url(r'^forgotten-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'forgotten_password_noscript', name='forgotten_password_change_form'),
)


urlpatterns += patterns('misago.users.views.options',
    url(r'^options/$', 'index', name='options'),
    url(r'^options/(?P<form_name>[-a-zA-Z]+)/$', 'form', name='options_form'),
)


urlpatterns += patterns('',
    url(r'^users/', include(patterns('misago.users.views.lists',
        url(r'^$', 'lander', name="users"),
        url(r'^active-posters/$', 'active_posters', name="users_active_posters"),
        url(r'^active-posters/(?P<page>\d+)/$', 'active_posters', name="users_active_posters"),
        url(r'^online/$', 'online', name="users_online"),
        url(r'^online/(?P<page>\d+)/$', 'online', name="users_online"),
        url(r'^(?P<rank_slug>[-a-zA-Z0-9]+)/$', 'rank', name="users_rank"),
        url(r'^(?P<rank_slug>[-a-zA-Z0-9]+)/(?P<page>\d+)/$', 'rank', name="users_rank"),
    )))
)


urlpatterns += patterns('',
    url(r'^user/(?P<user_slug>[a-zA-Z0-9]+)-(?P<user_id>\d+)/', include(patterns('misago.users.views.profile',
        url(r'^$', 'posts', name="user_posts"),
        url(r'^threads/$', 'threads', name="user_threads"),
        url(r'^followers/$', 'followers', name="user_followers"),
        url(r'^followers/(?P<page>\d+)/$', 'followers', name="user_followers"),
        url(r'^follows/$', 'follows', name="user_follows"),
        url(r'^follows/(?P<page>\d+)/$', 'follows', name="user_follows"),
        url(r'^name-history/$', 'name_history', name="user_name_history"),
        url(r'^name-history/(?P<page>\d+)/$', 'name_history', name="user_name_history"),
        url(r'^warnings/$', 'warnings', name="user_warnings"),
        url(r'^warnings/(?P<page>\d+)/$', 'warnings', name="user_warnings"),
        url(r'^ban-details/$', 'user_ban', name="user_ban"),

        url(r'^follow/$', 'follow_user', name="follow_user"),
        url(r'^block/$', 'block_user', name="block_user"),
    )))
)


urlpatterns += patterns('',
    url(r'^mod-user/(?P<user_slug>[a-zA-Z0-9]+)-(?P<user_id>\d+)/', include(patterns('misago.users.views.moderation',
        url(r'^warn/$', 'warn', name='warn_user'),
        url(r'^warn/(?P<warning_id>\d+)/cancel/$', 'cancel_warning', name='cancel_warning'),
        url(r'^warn/(?P<warning_id>\d+)/delete/$', 'delete_warning', name='delete_warning'),
        url(r'^rename/$', 'rename', name='rename_user'),
        url(r'^avatar/$', 'moderate_avatar', name='moderate_avatar'),
        url(r'^signature/$', 'moderate_signature', name='moderate_signature'),
        url(r'^ban/$', 'ban_user', name='ban_user'),
        url(r'^lift-ban/$', 'lift_user_ban', name='lift_user_ban'),
        url(r'^delete/$', 'delete', name='delete_user'),
    )))
)


urlpatterns += patterns('',
    url(r'^user-avatar/', include(patterns('misago.users.views.avatarserver',
        url(r'^(?P<hash>[a-f0-9]+)/(?P<size>\d+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar', name="user_avatar"),
        url(r'^tmp:(?P<token>[a-zA-Z0-9]+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar_source', kwargs={'suffix': 'tmp'}),
        url(r'^org:(?P<token>[a-zA-Z0-9]+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar_source', kwargs={'suffix': 'org'}),
        url(r'^(?P<size>\d+)\.png$', 'serve_blank_avatar', name="blank_avatar"),
    )))
)
