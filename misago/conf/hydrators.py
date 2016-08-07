import six


def hydrate_string(dry_value):
    return six.text_type(dry_value) if dry_value else ''


def dehydrate_string(wet_value):
    return wet_value


def hydrate_bool(dry_value):
    return dry_value == 'True'


def dehydrate_bool(wet_value):
    return 'True' if wet_value else 'False'


def hydrate_int(dry_value):
    return int(dry_value)


def dehydrate_int(wet_value):
    return six.text_type(wet_value)


def hydrate_list(dry_value):
    return [x for x in dry_value.split(',') if x]


def dehydrate_list(wet_value):
    return ','.join(wet_value)


VALUE_HYDRATORS = {
    'string': (hydrate_string, dehydrate_string),
    'bool': (hydrate_bool, dehydrate_bool),
    'int': (hydrate_int, dehydrate_int),
    'list': (hydrate_list, dehydrate_list),
}


def hydrate_value(python_type, dry_value):
    try:
        value_hydrator = VALUE_HYDRATORS[python_type][0]
    except KeyError:
        raise ValueError("%s type is not hydrateable" % python_type)

    return value_hydrator(dry_value)


def dehydrate_value(python_type, wet_value):
    try:
        value_dehydrator = VALUE_HYDRATORS[python_type][1]
    except KeyError:
        raise ValueError("%s type is not dehydrateable" % python_type)

    return value_dehydrator(wet_value)
