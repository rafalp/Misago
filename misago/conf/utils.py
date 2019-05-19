from . import hydrators


def get_setting_value(setting):
    return hydrators.hydrate_value(setting.python_type, setting.dry_value)


def set_setting_value(setting, new_value):
    if new_value is not None:
        setting.dry_value = hydrators.dehydrate_value(setting.python_type, new_value)
    else:
        setting.dry_value = None
    return setting.value
