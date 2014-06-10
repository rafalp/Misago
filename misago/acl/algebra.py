def sum_acls(defaults, acls, **permissions):
    result_acl = {}

    for permission, compare in permissions.items():
        try:
            permission_value = defaults[permission]
        except KeyError:
            message = 'Default value for permission "%s" is not provided.'
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
    elif b == 0:
        return b
    else:
        return greater(a, b)


def lower(a, b):
    return a if a < b else b

