from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from misago.forums.views.forumsadmin import (ForumsList, NewForum, EditForum,
                                             DeleteForum, MoveUpForum,
                                             MoveDownForum)
from misago.forums.views.permsadmin import (ForumRolesList, NewForumRole,
                                            EditForumRole, DeleteForumRole,
                                            RoleForumsACL)


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
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

    def register_navigation_nodes(self, site):
        site.add_node(name=_("Forums"),
                      icon='fa fa-comments',
                      parent='misago:admin',
                      before='misago:admin:permissions:users:index',
                      namespace='misago:admin:forums',
                      link='misago:admin:forums:nodes:index')

        site.add_node(name=_("Forums Hierarchy"),
                      icon='fa fa-sitemap',
                      parent='misago:admin:forums',
                      namespace='misago:admin:forums:nodes',
                      link='misago:admin:forums:nodes:index')

        site.add_node(name=_("Forum roles"),
                      icon='fa fa-comments-o',
                      parent='misago:admin:permissions',
                      after='misago:admin:permissions:users:index',
                      namespace='misago:admin:permissions:forums',
                      link='misago:admin:permissions:forums:index')
