from django.utils.translation import pgettext_lazy


class MisagoAdminExtension:
    def register_navigation_nodes(self, site):
        site.add_node(name=pgettext_lazy("admin node", "Dashboard"), icon="fa fa-home")
