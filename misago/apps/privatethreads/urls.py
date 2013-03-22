from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.privatethreads',
    url(r'^$', 'list.AllThreadsListView', name="private_threads"),
    url(r'^(?P<page>\d+)/$', 'list.AllThreadsListView', name="private_threads"),
    url(r'^new/$', 'list.NewThreadsListView', name="new_private_threads"),
    url(r'^new/(?P<page>\d+)/$', 'list.NewThreadsListView', name="new_private_threads"),
    url(r'^my/$', 'list.MyThreadsListView', name="my_private_threads"),
    url(r'^my/(?P<page>\d+)/$', 'list.MyThreadsListView', name="my_private_threads"),
    url(r'^start/$', 'posting.NewThreadView', name="private_thread_start"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/edit/$', 'posting.EditThreadView', name="private_thread_edit"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', 'posting.NewReplyView', name="private_thread_reply"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<quote>\d+)/reply/$', 'posting.NewReplyView', name="private_thread_reply"),
    url(r'^(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/edit/$', 'posting.EditReplyView', name="private_post_edit"),
)
