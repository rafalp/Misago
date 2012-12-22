from django.conf.urls import patterns, url

urlpatterns = patterns('misago.threads.views',
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'ThreadsView', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>\d+)/$', 'ThreadsView', name="forum"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/new/$', 'PostingView', name="thread_new", kwargs={'mode': 'new_thread'}),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', 'ThreadView', name="thread"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>\d+)/$', 'ThreadView', name="thread"),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', 'PostingView', name="thread_reply", kwargs={'mode': 'new_post'}),
)