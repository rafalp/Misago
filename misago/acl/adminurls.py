from django.conf.urls import url
from misago.admin import urlpatterns
from misago.acl.views import roles, forumroles


# Users section
urlpatterns.namespace(r'^permissions/', 'permissions')


# Roles
urlpatterns.namespace(r'^users/', 'users', 'permissions')
urlpatterns.patterns('permissions:users',
    url(r'^$', roles.RolesList.as_view(), name='index'),
    url(r'^new/$', roles.NewRole.as_view(), name='new'),
    url(r'^edit/(?P<role_id>\d+)/$', roles.EditRole.as_view(), name='edit'),
    url(r'^delete/(?P<role_id>\d+)/$', roles.DeleteRole.as_view(), name='delete'),
)


# Forum Roles
urlpatterns.namespace(r'^forums/', 'forums', 'permissions')
urlpatterns.patterns('permissions:forums',
    url(r'^$', forumroles.ForumRolesList.as_view(), name='index'),
    url(r'^new/$', forumroles.NewForumRole.as_view(), name='new'),
    url(r'^edit/(?P<role_id>\d+)/$', forumroles.EditForumRole.as_view(), name='edit'),
    url(r'^delete/(?P<role_id>\d+)/$', forumroles.DeleteForumRole.as_view(), name='delete'),
)
