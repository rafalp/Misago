from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views


class MisagoAdminExtension(object):
    def register_urlpatterns(self, urlpatterns):
        urlpatterns.namespace(r'^settings/', 'settings', 'system')

        urlpatterns.patterns(
            'system:settings',
            url(r'^$', views.index, name='index'),
            url(r'^(?P<key>(\w|-)+)/$', views.group, name='group'),
        )

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Settings"),
            icon='fa fa-sliders',
            parent='misago:admin:system',
            link='misago:admin:system:settings:index',
        )
