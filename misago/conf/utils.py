from . import hydrators


def get_setting_value(setting):
    if not setting.dry_value and setting.default_value:
        return hydrators.hydrate_value(setting.python_type, setting.default_value)
    else:
        return hydrators.hydrate_value(setting.python_type, setting.dry_value)


def set_setting_value(setting, new_value):
    if new_value is not None:
        setting.dry_value = hydrators.dehydrate_value(setting.python_type, new_value)
    else:
        setting.dry_value = None
    return setting.value


def has_custom_value(setting):
    return setting.dry_value and setting.dry_value != setting.default_value
