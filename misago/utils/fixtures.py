import base64
from django.utils import timezone
from django.utils.importlib import import_module
from misago.models import MonitorItem, SettingsGroup, Setting
from misago.utils.translation import get_msgid
try:
    import cPickle as pickle
except ImportError:
    import pickle

def load_fixture(name):
    """
    Load fixture
    """
    try:
        fixture = import_module(name)
        fixture.load()
        return True
    except (ImportError, AttributeError):
        return False


def update_fixture(name):
    """
    If fixture module contains update function, use it to update fixture
    """
    try:
        fixture = import_module(name)
        fixture.update()
        return True
    except (ImportError, AttributeError):
        return False


def load_settings_group_fixture(group, fixture):
    model_group = SettingsGroup(
                                key=group,
                                name=get_msgid(fixture['name']),
                                description=get_msgid(fixture.get('description'))
                                )
    model_group.save(force_insert=True)
    fixture = fixture.get('settings', ())
    position = 0
    for setting in fixture:
        value = setting[1].get('value')
        value_default = setting[1].get('default')
        # Convert boolean True and False to 1 and 0, otherwhise it wont work
        if setting[1].get('type') == 'boolean':
            value = 1 if value else 0
            value_default = 1 if value_default else 0
        # Convert array value to string
        if setting[1].get('type') == 'array':
            value = ','.join(value) if value else ''
            value_default = ','.join(value_default) if value_default else ''
        # Store setting in database
        model_setting = Setting(
                                setting=setting[0],
                                group=model_group,
                                value=value,
                                value_default=value_default,
                                normalize_to=setting[1].get('type'),
                                field=setting[1].get('input'),
                                extra=base64.encodestring(pickle.dumps(setting[1].get('extra', {}), pickle.HIGHEST_PROTOCOL)),
                                position=position,
                                separator=get_msgid(setting[1].get('separator')),
                                name=get_msgid(setting[1].get('name')),
                                description=get_msgid(setting[1].get('description')),
                                )
        model_setting.save(force_insert=True)
        position += 1


def update_settings_group_fixture(group, fixture):
    try:
        model_group = SettingsGroup.objects.get(key=group)
        settings = {}
        for setting in model_group.setting_set.all():
            settings[setting.pk] = setting.value
        model_group.delete()
        load_settings_group_fixture(group, fixture)

        for setting in settings:
            try:
                new_setting = Setting.objects.get(pk=setting)
                new_setting.value = settings[setting]
                new_setting.save(force_update=True)
            except Setting.DoesNotExist:
                pass
    except SettingsGroup.DoesNotExist:
        load_settings_group_fixture(group, fixture)


def load_settings_fixture(fixture):
    for group in fixture:
        load_settings_group_fixture(group[0], group[1])


def update_settings_fixture(fixture):
    for group in fixture:
        update_settings_group_fixture(group[0], group[1])


def load_monitor_fixture(fixture):
    for id in fixture.keys():
        item = MonitorItem.objects.create(
                                          id=id,
                                          value=fixture[id][0],
                                          type=fixture[id][1],
                                          updated=timezone.now()
                                          )


def update_monitor_fixture(fixture):
    for id in fixture.keys():
        try:
            item = MonitorItem.objects.get(id=id)
            item.type = fixture[id][1]
            item.updated = timezone.now()
            item.save(force_update=True)
        except MonitorItem.DoesNotExist:
            MonitorItem.objects.create(
                                       id=id,
                                       value=fixture[id][0],
                                       type=fixture[id][1],
                                       updated=timezone.now()
                                       )
