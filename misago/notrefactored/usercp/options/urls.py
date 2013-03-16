from django.conf.urls import patterns, url

def register_usercp_urls(first=False):
    if first:
        return patterns('misago.usercp.options.views',
            url(r'^$', 'options', name="usercp"),
            url(r'^$', 'options', name="usercp_options"),
        )
    return patterns('misago.usercp.options.views',
        url(r'^options/$', 'options', name="usercp_options"),
    )
