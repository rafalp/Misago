from misago.acl.providers import providers


def build_acl(roles):
    """
    Build ACL for given roles
    """
    acl = {}

    for provider, module in providers.list():
        module.build_acl(acl, roles)

    return acl
