from misago.acl.providers import providers


def build_acl(roles):
    """
    Build ACL for given roles
    """
    acl = {}

    for extension, module in providers.list():
        acl = module.build_acl(acl, roles, extension)

    return acl
