from .providers import providers


def build_acl(roles):
    """build ACL for given roles"""
    acl = {}

    for extension, module in providers.list():
        try:
            acl = module.build_acl(acl, roles, extension)
        except AttributeError:
            message = f"{extension} has to define build_acl function"
            raise AttributeError(message)

    return acl
