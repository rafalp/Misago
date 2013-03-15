from django.conf.urls import patterns, url

def register_usercp_urls(first=False):
    if first:
        return patterns('misago.usercp.username.views',
            url(r'^$', 'username', name="usercp"),
            url(r'^$', 'username', name="usercp_username"),
        )
    return patterns('misago.usercp.username.views',
        url(r'^username/$', 'username', name="usercp_username"),
    )
