from django.conf.urls import patterns, url, include

urlpatterns = patterns('misago.users.views',
    url(r'^users/$', 'users', name="users"),
    url(r'^users/(?P<username>\w+)-(?P<user>\d+)/$', 'user_profile', name="user"),
    url(r'^usercp/$', 'usercp_options', name="usercp"),
    url(r'^usercp/credentials$', 'usercp_credentials', name="usercp_credentials"),
    url(r'^usercp/username$', 'usercp_username', name="usercp_username"),
    url(r'^usercp/avatar$', 'usercp_avatar', name="usercp_avatar"),
    url(r'^usercp/signature$', 'usercp_signature', name="usercp_signature"),
    url(r'^usercp/ignored$', 'usercp_ignored', name="usercp_ignored"),
)