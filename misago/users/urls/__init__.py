from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.core.views',
    url(r'^banned/$', 'home_redirect', name='banned')
)


urlpatterns += patterns('misago.users.views.auth',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)


urlpatterns += patterns('misago.users.views.activation',
    url(r'^request-activation/$', 'request_activation', name="request-activation"),
    url(r'^activation/(?P<pk>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activate_by_token', name="activate-by-token"),
)


urlpatterns += patterns('misago.users.views.forgottenpassword',
    url(r'^forgotten-password/$', 'request_reset', name='forgotten-password'),
    url(r'^forgotten-password/(?P<pk>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'reset_password_form', name='forgotten-password-change-form'),
)


urlpatterns += patterns('misago.users.views.options',
    url(r'^options/$', 'index', name='options'),
    url(r'^options/(?P<form_name>[-a-zA-Z]+)/$', 'index', name='options-form'),

    url(r'^options/forum-options/$', 'index', name='usercp-change-forum-options'),
    url(r'^options/change-username/$', 'index', name='usercp-change-username'),
    url(r'^options/sign-in-credentials/$', 'index', name='usercp-change-email-password'),

    url(r'^options/change-email/(?P<token>[a-zA-Z0-9]+)/$', 'confirm_email_change', name='options-confirm-email-change'),
    url(r'^options/change-password/(?P<token>[a-zA-Z0-9]+)/$', 'confirm_password_change', name='options-confirm-password-change'),
)


urlpatterns += patterns('',
    url(r'^users/', include(patterns('misago.users.views.lists',
        url(r'^$', 'lander', name="users"),
        url(r'^active-posters/$', 'active_posters', name="users-active-posters"),
        url(r'^(?P<slug>[-a-zA-Z0-9]+)/$', 'rank', name="users-rank"),
        url(r'^(?P<slug>[-a-zA-Z0-9]+)/(?P<page>\d+)/$', 'rank', name="users-rank"),
    )))
)


urlpatterns += patterns('',
    url(r'^user/(?P<slug>[a-zA-Z0-9]+)-(?P<pk>\d+)/', include(patterns('misago.users.views.profile',
        url(r'^$', 'lander', name="user"),
        url(r'^posts/$', 'posts', name="user-posts"),
        url(r'^threads/$', 'threads', name="user-threads"),
        url(r'^followers/$', 'followers', name="user-followers"),
        url(r'^follows/$', 'follows', name="user-follows"),
        url(r'^username-history/$', 'username_history', name="username-history"),
        url(r'^ban-details/$', 'user_ban', name="user-ban"),
    )))
)


urlpatterns += patterns('',
    url(r'^user-avatar/', include(patterns('misago.users.views.avatarserver',
        url(r'^(?P<hash>[a-f0-9]+)/(?P<size>\d+)/(?P<pk>\d+)\.png$', 'serve_user_avatar', name="user-avatar"),
        url(r'^(?P<secret>[a-f0-9]+):(?P<hash>[a-f0-9]+)/(?P<pk>\d+)\.png$', 'serve_user_avatar_source', name="user-avatar-source"),
        url(r'^(?P<size>\d+)\.png$', 'serve_blank_avatar', name="blank-avatar"),
    )))
)
