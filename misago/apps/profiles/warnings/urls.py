from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.profiles.warnings.views',
            url(r'^$', 'warnings', name="user"),
            url(r'^$', 'warnings', name="user_warnings"),
            url(r'^(?P<page>[1-9]([0-9]+)?)/$', 'warnings', name="user_warnings"),
            url(r'^(?P<warning>\d+)/cancel/$', 'cancel_warning', name="user_warnings_cancel"),
            url(r'^(?P<warning>\d+)/delete/$', 'delete_warning', name="user_warnings_delete"),
        )
    else:
        urlpatterns += patterns('misago.apps.profiles.warnings.views',
            url(r'^warnings/$', 'warnings', name="user_warnings"),
            url(r'^warnings/(?P<page>[1-9]([0-9]+)?)/$', 'warnings', name="user_warnings"),
            url(r'^warnings/(?P<warning>\d+)/cancel/$', 'cancel_warning', name="user_warnings_cancel"),
            url(r'^warnings/(?P<warning>\d+)/delete/$', 'delete_warning', name="user_warnings_delete"),
        )
    return urlpatterns