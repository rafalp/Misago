from django.conf.urls import patterns, url

def register_usercp_urls(first=False):
    if first:
        return patterns('misago.apps.usercp.signature.views',
            url(r'^$', 'signature', name="usercp"),
            url(r'^$', 'signature', name="usercp_signature"),
        )
    
    return patterns('misago.apps.usercp.signature.views',
        url(r'^signature/$', 'signature', name="usercp_signature"),
    )
