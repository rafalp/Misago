from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^category/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', views.category_redirect),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', views.category_redirect),
    url(
        r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>[1-9]([0-9]+)?)/$',
        views.category_redirect
    ),
    url(
        r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/prefix/(?P<prefix>(\w|-)+)/$',
        views.category_redirect
    ),
    url(
        r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/prefix/(?P<prefix>(\w|-)+)/(?P<page>[1-9]([0-9]+)?)/$',
        views.category_redirect
    ),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/start/$', views.category_redirect),
]

urlpatterns += [
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/edit/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/vote/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/poll/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/reply/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/edit/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', views.thread_redirect),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>[1-9]([0-9]+)?)/$',
        views.thread_redirect
    ),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/last/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/find-(?P<post>\d+)/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/new/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/moderated/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reported/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/show-hidden/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/email/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/email/$', views.thread_redirect),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/upvote/$', views.thread_redirect
    ),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/downvote/$',
        views.thread_redirect
    ),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/report/$', views.thread_redirect
    ),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show-report/$',
        views.thread_redirect
    ),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/delete/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/hide/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/show/$', views.thread_redirect),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/delete/$', views.thread_redirect
    ),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/hide/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show/$', views.thread_redirect),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/delete/$',
        views.thread_redirect
    ),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/hide/$',
        views.thread_redirect
    ),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/show/$',
        views.thread_redirect
    ),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/info/$', views.thread_redirect),
    url(r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/votes/$', views.thread_redirect),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/$',
        views.thread_redirect
    ),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/$',
        views.thread_redirect
    ),
    url(
        r'^thread/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/revert/$',
        views.thread_redirect
    ),
]

urlpatterns += [
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/edit/$', views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reply/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/vote/$', views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/poll/$', views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/reply/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/edit/$',
        views.private_thread_redirect
    ),
    url(r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/$', views.private_thread_redirect),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<page>[1-9]([0-9]+)?)/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/last/$', views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/find-(?P<post>\d+)/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/new/$', views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/moderated/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/reported/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/show-hidden/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/watch/email/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/unwatch/email/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/upvote/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/downvote/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/report/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show-report/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/delete/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/hide/$', views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/show/$', views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/delete/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/hide/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/show/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/delete/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/hide/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/checkpoint/(?P<checkpoint>\d+)/show/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/info/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/votes/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/$',
        views.private_thread_redirect
    ),
    url(
        r'^private-threads/(?P<slug>(\w|-)+)-(?P<thread>\d+)/(?P<post>\d+)/changelog/(?P<change>\d+)/revert/$',
        views.private_thread_redirect
    ),
]

urlpatterns += [
    url(r'^users/(?P<username>\w+)-(?P<user>\d+)/', views.user_redirect),
    url(r'^users/(?P<username>\w+)-(?P<user>\d+)/(?P<page>\d+)/', views.user_redirect),
    url(r'^users/(?P<username>\w+)-(?P<user>\d+)/(?P<subpage>(\w|-)+)/', views.user_redirect),
    url(
        r'^users/(?P<username>\w+)-(?P<user>\d+)/(?P<subpage>(\w|-)+)/(?P<page>\d+)/',
        views.user_redirect
    ),
]
