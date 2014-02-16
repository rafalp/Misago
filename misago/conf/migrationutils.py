from importlib import import_module
from misago.conf.dbsettings import CACHE_KEY
from misago.core.cache import cache as default_cache


def with_conf_models(migration, this_migration=None):
    module_name = 'misago.conf.migrations.%s' % migration
    migration_module = import_module(module_name)
    conf_models = migration_module.Migration.models

    if this_migration:
        conf_models.update(this_migration)
    return conf_models


def get_custom_settings_values(orm, group):
    custom_settings_values = {}

    for setting in group.setting_set.iterator():
        if setting.has_custom_value:
            custom_settings_values[setting.setting] = setting.value

    return custom_settings_values


def get_group(orm, group_key):
    try:
        return orm['conf.SettingsGroup'].objects.get(key=group_key)
    except orm['conf.SettingsGroup'].DoesNotExist:
        return orm['conf.SettingsGroup']()


def migrate_settings_group(orm, group_fixture, old_group_key=None):
    group_key = group_fixture['key']

    # Fetch settings group

    if old_group_key:
        group = get_group(orm, old_group_key)
        custom_settings_values = get_custom_settings_values(orm, group)
    else:
        group = get_group(orm, group_key)
        if group.pk:
            custom_settings_values = get_custom_settings_values(orm, group)
        else:
            custom_settings_values = {}


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
            value = custom_settings_values[setting['setting']]
        except KeyError:
            value = setting.pop('value', None)
        field_extra = setting.pop('field_extra', None)

        setting = orm['conf.Setting'](**setting)
        setting.value = value
        setting.field_extra = field_extra
        setting.save()


def delete_settings_cache():
    default_cache.delete(CACHE_KEY)
