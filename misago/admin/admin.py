from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _


class MisagoAdminExtension(MiddlewareMixin):
    def register_urlpatterns(self, urlpatterns):
        pass

    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Home"),
            icon='fa fa-home',
            parent='misago:admin',
            link='misago:admin:index',
        )
