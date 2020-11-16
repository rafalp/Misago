from importlib import import_module

from django.apps import apps

from .site import site
from .urlpatterns import urlpatterns


def discover_misago_admin():
    for app in apps.get_app_configs():
        module = import_module(app.name)
        if not hasattr(module, "admin"):
            continue

        admin_module = import_module("%s.admin" % app.name)
        if hasattr(admin_module, "MisagoAdminExtension"):
            extension = getattr(admin_module, "MisagoAdminExtension")()
            if hasattr(extension, "register_navigation_nodes"):
                extension.register_navigation_nodes(site)
            if hasattr(extension, "register_urlpatterns"):
                extension.register_urlpatterns(urlpatterns)
