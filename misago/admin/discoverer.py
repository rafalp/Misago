from importlib import import_module

from django.apps import apps

from .hierarchy import site
from .urlpatterns import urlpatterns


__ALL__ = ['discover_misago_admin']


def discover_misago_admin():
    for app in apps.get_app_configs():
        module = import_module(app.name)
        if hasattr(module, 'admin'):
            admin_module = import_module('%s.admin' % app.name)
            if hasattr(admin_module, 'MisagoAdminExtension'):
                extension = getattr(admin_module, 'MisagoAdminExtension')()
                extension.register_navigation_nodes(site)
                extension.register_urlpatterns(urlpatterns)
