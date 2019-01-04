from django.utils.translation import gettext_lazy as _


class MisagoAdminExtension:
    def register_navigation_nodes(self, site):
        site.add_node(
            name=_("Home"),
            icon="fa fa-home",
            parent="misago:admin",
            link="misago:admin:index",
        )
