from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from misago.categories.views.categoriesadmin import (
    CategoriesList, NewCategory, EditCategory, MoveDownCategory,
    MoveUpCategory, DeleteCategory)
from misago.categories.views.permsadmin import (
    CategoryRolesList, NewCategoryRole, EditCategoryRole, DeleteCategoryRole,
    CategoryPermissions, RoleCategoriesACL)


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        # Categories section
        urlpatterns.namespace(r'^categories/', 'categories')

        # Nodes
        urlpatterns.namespace(r'^nodes/', 'nodes', 'categories')
        urlpatterns.patterns('categories:nodes',
            url(r'^$', CategoriesList.as_view(), name='index'),
            url(r'^new/$', NewCategory.as_view(), name='new'),
            url(r'^edit/(?P<category_id>\d+)/$', EditCategory.as_view(), name='edit'),
            url(r'^permissions/(?P<category_id>\d+)/$', CategoryPermissions.as_view(), name='permissions'),
            url(r'^move/down/(?P<category_id>\d+)/$', MoveDownCategory.as_view(), name='down'),
            url(r'^move/up/(?P<category_id>\d+)/$', MoveUpCategory.as_view(), name='up'),
            url(r'^delete/(?P<category_id>\d+)/$', DeleteCategory.as_view(), name='delete'),
        )

        # Category Roles
        urlpatterns.namespace(r'^categories/', 'categories', 'permissions')
        urlpatterns.patterns('permissions:categories',
            url(r'^$', CategoryRolesList.as_view(), name='index'),
            url(r'^new/$', NewCategoryRole.as_view(), name='new'),
            url(r'^edit/(?P<role_id>\d+)/$', EditCategoryRole.as_view(), name='edit'),
            url(r'^delete/(?P<role_id>\d+)/$', DeleteCategoryRole.as_view(), name='delete'),
        )

        # Change Role Category Permissions
        urlpatterns.patterns('permissions:users',
            url(r'^categories/(?P<role_id>\d+)/$', RoleCategoriesACL.as_view(), name='categories'),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Categories"),
            icon='fa fa-comments',
            parent='misago:admin',
            before='misago:admin:permissions:users:index',
            namespace='misago:admin:categories',
            link='misago:admin:categories:nodes:index'
        )

        site.add_node(
            name=_("Categories hierarchy"),
            icon='fa fa-sitemap',
            parent='misago:admin:categories',
            namespace='misago:admin:categories:nodes',
            link='misago:admin:categories:nodes:index'
        )

        site.add_node(
            name=_("Category roles"),
            icon='fa fa-comments-o',
            parent='misago:admin:permissions',
            after='misago:admin:permissions:users:index',
            namespace='misago:admin:permissions:categories',
            link='misago:admin:permissions:categories:index'
        )
