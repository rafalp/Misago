from django.conf.urls import patterns, url

urlpatterns = patterns('misago.threads.views',
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'List', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>\d+)/$', 'List', name="forum"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', 'Thread', name="thread"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>\d+)/$', 'Thread', name="topic"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', 'Posting', name="topic_reply"),
)