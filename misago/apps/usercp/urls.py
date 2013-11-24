from django.conf import settings
from django.conf.urls import include, patterns, url
from django.utils.importlib import import_module

urlpatterns = []
iteration = 0
for extension in settings.USERCP_EXTENSIONS:
    iteration += 1
    usercp_module = import_module(extension + '.urls')
    try:
        urlpatterns += patterns('',
            (r'^', include(usercp_module.register_usercp_urls(iteration == 1))),
        )
    except AttributeError:
        pass

urlpatterns += patterns('misago.apps.usercp.views',
    url(r'^follow/(?P<user>\d+)/$', 'follow', name="follow_user"),
    url(r'^unfollow/(?P<user>\d+)/$', 'unfollow', name="unfollow_user"),
    url(r'^ignore/(?P<user>\d+)/$', 'ignore', name="ignore_user"),
    url(r'^unignore/(?P<user>\d+)/$', 'unignore', name="unignore_user"),
)