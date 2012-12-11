from django.conf import settings
from django.utils.importlib import import_module
from misago.forms import Form

def build_form(request, role):
    form_type = type('ACLForm', (Form,), dict(layout=[]))
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.make_form(request, role, form_type)
        except AttributeError:
            pass
    return form_type


class BaseACL(object):
    def __init__(self):
        self.acl = {}


class ACL(object):
    def __init__(self, version):
        self.version = version


def build_acl(request, roles):
    acl = ACL(request.monitor['acl_version'])
    perms = []
    for role in roles:
        perms.append(role.get_permissions())
    for provider in settings.PERMISSION_PROVIDERS:
        app_module = import_module(provider)
        try:
            app_module.build(acl, perms)
        except AttributeError:
            pass
    return acl