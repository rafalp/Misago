from django.conf.urls import url
from misago.admin import urlpatterns
from misago.acl.views import RolesList, NewRole, EditRole, DeleteRole


# Users section
urlpatterns.namespace(r'^permissions/', 'permissions')


# Roles
urlpatterns.namespace(r'^users/', 'users', 'permissions')
urlpatterns.patterns('permissions:users',
    url(r'^$', RolesList.as_view(), name='index'),
    url(r'^new/$', NewRole.as_view(), name='new'),
    url(r'^edit/(?P<role_id>\d+)/$', EditRole.as_view(), name='edit'),
    url(r'^delete/(?P<role_id>\d+)/$', DeleteRole.as_view(), name='delete'),
)
