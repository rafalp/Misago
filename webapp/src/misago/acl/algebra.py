def _roles_acls(key_name, roles):
    acls = []
    for role in roles:
        role_permissions = role.permissions.get(key_name)
        if role_permissions:
            acls.append(role_permissions)
    return acls


def sum_acls(result_acl, acls=None, roles=None, key=None, **permissions):
    if acls and roles:
        raise ValueError('You can not provide both "acls" and "roles" arguments')

    if (acls is None) and (roles is None):
        raise ValueError('You have to provide either "acls" and "roles" argument')

    if roles is not None:
        if not key:
            raise ValueError(
                'You have to provide "key" argument if you '
                "are passing roles instead of acls"
            )
        acls = _roles_acls(key, roles)

    for permission, compare in permissions.items():
        try:
            permission_value = result_acl[permission]
        except KeyError:
            message = 'Default value for permission "%s" is not provided'
            raise ValueError(message % permission)

        for acl in acls:
            try:
                permission_value = compare(permission_value, acl[permission])
            except KeyError:
                pass
        result_acl[permission] = permission_value

    return result_acl


# Common comparisions
def greater(a, b):
    return a if a > b else b


def greater_or_zero(a, b):
    if a == 0:
        return a
    if b == 0:
        return b
    return greater(a, b)


def lower(a, b):
    return a if a < b else b


def lower_non_zero(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    return lower(a, b)
