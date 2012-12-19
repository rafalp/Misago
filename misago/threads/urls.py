from django.conf.urls import patterns, url

urlpatterns = patterns('misago.threads.views',
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'threads', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>\d+)/$', 'threads', name="forum"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', 'thread', name="thread"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>\d+)/$', 'thread', name="topic"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', 'thread', name="topic_reply"),
)