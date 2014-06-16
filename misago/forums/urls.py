from django.conf.urls import url
from misago.admin import urlpatterns
from misago.forums.views.forumsadmin import (ForumsList, NewForum, EditForum,
                                             DeleteForum, MoveUpForum,
                                             MoveDownForum)
from misago.forums.views.permsadmin import (ForumRolesList, NewForumRole,
                                            EditForumRole, DeleteForumRole,
                                            RoleForumsACL)


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

# Forum Roles
urlpatterns.namespace(r'^forums/', 'forums', 'permissions')
urlpatterns.patterns('permissions:forums',
    url(r'^$', ForumRolesList.as_view(), name='index'),
    url(r'^new/$', NewForumRole.as_view(), name='new'),
    url(r'^edit/(?P<role_id>\d+)/$', EditForumRole.as_view(), name='edit'),
    url(r'^delete/(?P<role_id>\d+)/$', DeleteForumRole.as_view(), name='delete'),
)


# Change Role Forum Permissions
urlpatterns.patterns('permissions:users',
    url(r'^forums/(?P<role_id>\d+)/$', RoleForumsACL.as_view(), name='forums'),
)
