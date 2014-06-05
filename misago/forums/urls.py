from django.conf.urls import url
from misago.admin import urlpatterns
from misago.forums.views import (ForumsList, NewForum, EditForum, DeleteForum,
                                 MoveUpForum, MoveDownForum)


# Forums section
urlpatterns.namespace(r'^forums/', 'forums')


# Nodes
urlpatterns.namespace(r'^nodes/', 'nodes', 'forums')
urlpatterns.patterns('forums:nodes',
    url(r'^$', ForumsList.as_view(), name='index'),
    url(r'^new/$', NewForum.as_view(), name='new'),
    url(r'^edit/(?P<forum_id>\d+)/$', EditForum.as_view(), name='edit'),
    url(r'^move/up/(?P<forum_id>\d+)/$', MoveUpForum.as_view(), name='up'),
    url(r'^move/down/(?P<forum_id>\d+)/$', MoveDownForum.as_view(), name='down'),
    url(r'^delete/(?P<forum_id>\d+)/$', DeleteForum.as_view(), name='delete'),
)
