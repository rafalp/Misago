from importlib import import_module
from django.conf import settings


__ALL__ = ['providers', 'get_default_permissions',
           'get_change_permissions_forms']


# Manager for permission providers
class PermissionProviders(object):
    def __init__(self):
        self._initialized = False
        self._providers = []
        self._providers_dict = {}

    def _assert_providers_imported(self):
        if not self._initialized:
            self._import_providers()
            self._initialized = True

    def _import_providers(self):
        for namespace in settings.MISAGO_PERMISSION_PROVIDERS:
            self._providers.append((namespace, import_module(namespace)))
            self._providers_dict[namespace] = import_module(namespace)

    def list(self):
        self._assert_providers_imported()
        return self._providers

    def dict(self):
        self._assert_providers_imported()
        return self._providers_dict


providers = PermissionProviders()


"""
Module functions for ACLS

Workflow for ACLs in Misago is simple:

First, you get user ACL. You can introspect it directory to find out user
permissions, or if you have objects, you can use this acl to make those objects
aware of their ACLs. This gives objects themselves special "acl" attribute with
properties defined by ACL providers within their "add_acl_to_target"
"""
def get_user_acl(user):
    """
    Get hydrated ACL for User
    """
    pass


def _add_acl_to_target(acl, target):
    """
    Add valid ACL to single target
    """
    for provider, module in providers.list():
        module.add_acl_to_target(acl, target)


def add_acl(acl, target):
    """
    Add valid ACL to target (iterable of objects or single object)
    """
    targets = []

    try:
        for item in target:
            targets.append(item)
    except TypeError:
        targets.append(target)

    for target in targets:
        _add_acl_to_target(acl, target)


"""
Admin utils
"""
def get_change_permissions_forms(role, data=None):
    """
    Utility function for building forms in admin
    """
    role_permissions = role.permissions

    forms = []
    for provider, module in providers.list():
        try:
            default_data = module.DEFAULT_PERMISSIONS
        except AttributeError:
            message = "'%s' object has no attribute '%s'"
            raise AttributeError(
                message % (provider, 'DEFAULT_PERMISSIONS'))
        try:
            module.change_permissions_form
        except AttributeError:
            message = "'%s' object has no attribute '%s'"
            raise AttributeError(
                message % (provider, 'change_permissions_form'))

        FormType = module.change_permissions_form(role)

        if FormType:
            if data:
                forms.append(FormType(data, prefix=provider))
            else:
                initial_data = role_permissions.get(provider, default_data)
                forms.append(FormType(initial=initial_data,
                                      prefix=provider))

    return forms
