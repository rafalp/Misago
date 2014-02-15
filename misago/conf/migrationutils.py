from misago.conf import CACHE_KEY
from misago.core.cache import cache as default_cache


def get_custom_settings_values(orm, group_key):
    custom_settings_values = {}

    for setting in orm.Setting.objects.filter(group_id=group_key).iterator():
        custom_settings_values[setting.setting] = setting.value

    return custom_settings_values


def get_group(orm, group_key):
    try:
        return orm.SettingsGroup.objects.get(key=group_key)
    except orm.SettingsGroup.DoesNotExist:
        return orm.SettingsGroup()


def migrate_settings_group(orm, group_fixture, old_group_key=None):
    group_key = group_fixture['key']

    # Fetch settings group

    if old_group_key:
        custom_settings_values = get_custom_settings_values(orm, old_group_key)
        group = get_group(orm, old_group_key)
    else:
        custom_settings_values = get_custom_settings_values(orm, group_key)
        group = get_group(orm, group_key)


    # Update group's attributes

    group.key = group_fixture['key']
    group.name = group_fixture['name']
    group.description = group_fixture.get('description')
    group.save()


    # Delete groups settings and make new ones
    # Its easier to create news ones and then assign them old values

    group.setting_set.all().delete()

    for order, setting in enumerate(group_fixture['settings']):
        setting['group'] = group
        setting['order'] = order

        try:
            value = custom_settings_values[seting['setting']]
        except KeyError:
            value = setting.pop('value')
        field_extra = setting.pop('field_extra', None)

        setting = orm.Setting(**setting)
        setting.value = value
        setting.field_extra = field_extra
        setting.save()


def clear_settings_cache():
    default_cache.delete(CACHE_KEY)
