from django.conf.urls import patterns, url, include

urlpatterns = patterns('misago.users.views',
    url(r'^register/$', 'register', name="register"),
    url(r'^activate/(?P<username>\w+)-(?P<user>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activation.activate', name="activate"),
    url(r'^resend-activation/$', 'activation.form', name="send_activation"),
    url(r'^reset-pass/$', 'password.form', name="forgot_password"),
    url(r'^reset-pass/(?P<username>\w+)-(?P<user>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'password.reset', name="reset_password"),
    url(r'^users/$', 'profiles.list', name="users"),
    url(r'^users/(?P<username>\w+)-(?P<user>\d+)/$', 'profiles.show', name="user"),
    url(r'^users/(?P<rank_slug>(\w|-)+)/$', 'profiles.list', name="users"),
    url(r'^usercp/$', 'usercp.options', name="usercp"),
    url(r'^usercp/credentials$', 'usercp.credentials', name="usercp_credentials"),
    url(r'^usercp/username$', 'usercp.username', name="usercp_username"),
    url(r'^usercp/avatar$', 'usercp.avatar', name="usercp_avatar"),
    url(r'^usercp/signature$', 'usercp.signature', name="usercp_signature"),
    url(r'^usercp/ignored$', 'usercp.ignored', name="usercp_ignored"),
)