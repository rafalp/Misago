from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from misago.conf import views


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.namespace(r'^settings/', 'settings')

        urlpatterns.patterns('settings',
            url(r'^$', views.index, name='index'),
            url(r'^(?P<key>(\w|-)+)/$', views.group, name='group'),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Settings"),
            icon='fa fa-gears',
            parent='misago:admin',
            link='misago:admin:settings:index',
        )
