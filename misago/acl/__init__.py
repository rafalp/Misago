from misago.acl.providers import providers  # noqa


def get_change_permissions_forms(role):
    return providers.get_change_permissions_forms(role)


def build_acl_cache(roles):
    return providers.build_acl_cache(roles)


def hydrate_acl_cache(acl):
    return providers.hydrate_acl_cache(acl)


def get_acl_by_token(token):
    return providers.get_acl_by_token(token)


def get_acl_by_roles(roles):
    return providers.get_acl_by_roles(roles)
