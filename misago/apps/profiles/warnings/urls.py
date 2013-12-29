from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.profiles.warnings.views',
            url(r'^$', 'warnings', name="user"),
            url(r'^$', 'warnings', name="user_warnings"),
            url(r'^(?P<page>[1-9]([0-9]+)?)/$', 'warnings', name="user_warnings"),
        )
    else:
        urlpatterns += patterns('misago.apps.profiles.warnings.views',
            url(r'^warnings/$', 'warnings', name="user_warnings"),
            url(r'^warnings/(?P<page>[1-9]([0-9]+)?)/$', 'warnings', name="user_warnings"),
        )
    return urlpatterns