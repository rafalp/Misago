from misago.conf.dbsettings import CACHE_KEY
from misago.conf.hydrators import dehydrate_value
from misago.core import serializer
from misago.core.cache import cache as default_cache


def get_group(SettingsGroup, group_key):
    try:
        return SettingsGroup.objects.get(key=group_key)
    except SettingsGroup.DoesNotExist:
        return SettingsGroup()


def get_custom_settings_values(group):
    custom_settings_values = {}

    for setting in group.setting_set.iterator():
        if setting.has_custom_value:
            custom_settings_values[setting.setting] = setting.value

    return custom_settings_values


def migrate_setting(Setting, group, setting_fixture, order, old_value):
    setting_fixture['group'] = group
    setting_fixture['order'] = order

    setting_fixture['name'] = setting_fixture['name']
    if setting_fixture.get('description'):
        setting_fixture['description'] = setting_fixture.get('description')

    if (setting_fixture.get('field_extra') and
            setting_fixture.get('field_extra').get('choices')):
        untranslated_choices = setting_fixture['field_extra']['choices']
        translated_choices = []
        for val, name in untranslated_choices:
            translated_choices.append((val, name))
        setting_fixture['field_extra']['choices'] = tuple(
            translated_choices)

    if old_value is None:
        value = setting_fixture.pop('value', None)
    else:
        value = old_value
    setting_fixture.pop('value', None)

    field_extra = setting_fixture.pop('field_extra', None)

    setting = Setting(**setting_fixture)
    setting.dry_value = dehydrate_value(setting.python_type, value)

    if setting_fixture.get("default_value"):
        setting.default_value = dehydrate_value(
            setting.python_type, setting_fixture.get("default_value"))

    if field_extra:
        setting.pickled_field_extra = serializer.dumps(field_extra)

    setting.save()


def migrate_settings_group(apps, group_fixture, old_group_key=None):
    SettingsGroup = apps.get_model('misago_conf', 'SettingsGroup')
    Setting = apps.get_model('misago_conf', 'Setting')
    group_key = group_fixture['key']

    # Fetch settings group

    if old_group_key:
        group = get_group(SettingsGroup, old_group_key)
        custom_settings_values = get_custom_settings_values(group)
    else:
        group = get_group(SettingsGroup, group_key)
        if group.pk:
            custom_settings_values = get_custom_settings_values(group)
        else:
            custom_settings_values = {}

    # Update group's attributes

    group.key = group_fixture['key']
    group.name = group_fixture['name']
    if group_fixture.get('description'):
        group.description = group_fixture.get('description')
    group.save()

    # Delete groups settings and make new ones
    # Its easier to create news ones and then assign them old values

    group.setting_set.all().delete()

    for order, setting_fixture in enumerate(group_fixture['settings']):
        old_value = custom_settings_values.pop(setting_fixture['name'], None)
        migrate_setting(Setting, group, setting_fixture, order, old_value)


def delete_settings_cache():
    default_cache.delete(CACHE_KEY)
