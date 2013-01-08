from django.conf.urls import patterns, url

urlpatterns = patterns('misago.profiles.views',
    url(r'^$', 'list', name="users"),
    url(r'^(?P<username>\w+)-(?P<user>\d+)/$', 'profile', name="user"),
    url(r'^(?P<username>\w+)-(?P<user>\d+)/threads/$', 'profile', name="user_threads", kwargs={'tab': 'threads'}),
    url(r'^(?P<username>\w+)-(?P<user>\d+)/following/$', 'profile', name="user_following", kwargs={'tab': 'following'}),
    url(r'^(?P<username>\w+)-(?P<user>\d+)/followiers/$', 'profile', name="user_followers", kwargs={'tab': 'followers'}),
    url(r'^(?P<username>\w+)-(?P<user>\d+)/details/$', 'profile', name="user_details", kwargs={'tab': 'details'}),
    url(r'^(?P<rank_slug>(\w|-)+)/$', 'list', name="users"),
)
