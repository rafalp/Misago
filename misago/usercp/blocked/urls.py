from django.conf.urls import patterns, url

def register_usercp_urls(first=False):
    if first:
        return patterns('misago.usercp.blocked.views',
            url(r'^$', 'blocked', name="usercp"),
            url(r'^$', 'blocked', name="usercp_blocked"),
        )
    return patterns('misago.usercp.blocked.views',
        url(r'^blocked/$', 'blocked', name="usercp_blocked"),
    )
