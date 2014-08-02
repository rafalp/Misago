from django.conf import settings
from django.conf.urls import include, patterns, url


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
    url(r'^forgotten-password/link-sent/$', 'link_sent', name='reset_password_link_sent'),
    url(r'^forgotten-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'reset_password_form', name='reset_password_form'),
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
    url(r'^usercp/change-avatar/$', 'change_avatar', name="usercp_change_avatar"),
    url(r'^usercp/change-avatar/upload/$', 'upload_avatar', name="usercp_upload_avatar"),
    url(r'^usercp/change-avatar/upload/handle/$', 'upload_avatar_handler', name="usercp_upload_avatar_handler"),
    url(r'^usercp/change-avatar/upload/crop/$', 'crop_avatar', name="usercp_crop_new_avatar", kwargs={'use_tmp_avatar': True}),
    url(r'^usercp/change-avatar/crop/$', 'crop_avatar', name="usercp_crop_avatar", kwargs={'use_tmp_avatar': False}),
    url(r'^usercp/change-avatar/galleries/$', 'avatar_galleries', name="usercp_avatar_galleries"),
    url(r'^usercp/edit-signature/$', 'edit_signature', name="usercp_edit_signature"),
    url(r'^usercp/change-username/$', 'change_username', name="usercp_change_username"),
    url(r'^usercp/change-email-password/$', 'change_email_password', name="usercp_change_email_password"),
    url(r'^usercp/change-email-password/(?P<token>[a-zA-Z0-9]+)/$', 'confirm_email_password_change', name='usercp_confirm_email_password_change'),
)


urlpatterns += patterns('',
    url(r'^user/(?P<user_slug>[a-zA-Z0-9]+)-(?P<user_id>\d+)/', include(patterns('misago.users.views.profile',
        url(r'^$', 'user_posts', name="user_posts"),
        url(r'^threads/$', 'user_threads', name="user_threads"),
        url(r'^name-history/$', 'name_history', name="user_name_history"),
        url(r'^name-history/(?P<page>\d+)/$', 'name_history', name="user_name_history"),
        url(r'^ban-details/$', 'user_ban', name="user_ban"),
    )))
)


urlpatterns += patterns('',
    url(r'^mod-user/(?P<user_slug>[a-zA-Z0-9]+)-(?P<user_id>\d+)/', include(patterns('misago.users.views.moderation',
        url(r'^rename/$', 'rename', name='rename_user'),
        url(r'^ban-user/$', 'ban_user', name='ban_user'),
        url(r'^delete/$', 'delete', name='delete_user'),
    ))),
)


urlpatterns += patterns('',
    url(r'^user-avatar/', include(patterns('misago.users.views.avatarserver',
        url(r'^(?P<size>\d+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar', name="user_avatar"),
        url(r'^tmp:(?P<token>[a-zA-Z0-9]+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar_source', name="user_avatar_tmp", kwargs={'type': 'tmp'}),
        url(r'^org:(?P<token>[a-zA-Z0-9]+)/(?P<user_id>\d+)\.png$', 'serve_user_avatar_source', name="user_avatar_org", kwargs={'type': 'org'}),
        url(r'^(?P<size>\d+)\.png$', 'serve_blank_avatar', name="blank_avatar"),
    )))
)
