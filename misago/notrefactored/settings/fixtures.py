import base64
from misago.settings.models import Group, Setting
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid
try:
    import cPickle as pickle
except ImportError:
    import pickle

settings_fixture = (
   # Basic options
   ('basic', {
        'name': _("Basic Settings"),
        'settings': (
            ('board_name', {
                'value':        "Misago",
                'type':         "string",
                'input':        "text",
                'separator':    _("Board Name"),
                'name':         _("Board Name"),
            }),
            ('board_header', {
                'type':         "string",
                'input':        "text",
                'name':         _("Board Header"),
                'description':  _("Some themes allow you to define text in board header. Leave empty to use Board Name instead."),
            }),
            ('board_header_postscript', {
                'value':        "Work in progress",
                'type':         "string",
                'input':        "text",
                'name':         _("Board Header Postscript"),
                'description':  _("Additional text displayed in some themes board header after board name."),
            }),
            ('board_index_title', {
                'type':         "string",
                'input':        "text",
                'separator':    _("Board Index"),
                'name':         _("Board Index Title"),
                'description':  _("If you want to, you can replace page title content on Board Index with custom one."),
            }),
            ('board_index_meta', {
                'type':         "string",
                'input':        "text",
                'name':         _("Board Index Meta-Description"),
                'description':  _("Meta-Description used to describe your board's index page."),
            }),
            ('board_credits', {
                'type':         "string",
                'input':        "textarea",
                'separator':    _("Board Footer"),
                'name':         _("Custom Credit"),
                'description':  _("Custom Credit to display in board footer above software and theme copyright information. You can use HTML."),
            }),
            ('email_footnote', {
                'type':         "string",
                'input':        "textarea",
                'separator':    _("Board E-Mails"),
                'name':         _("Custom Footnote in HTML E-mails"),
                'description':  _("Custom Footnote to display in HTML e-mail messages sent by board."),
            }),
            ('email_footnote_plain', {
                'type':         "string",
                'input':        "textarea",
                'name':         _("Custom Footnote in plain text E-mails"),
                'description':  _("Custom Footnote to display in plain text e-mail messages sent by board."),
            }),
        ),
   }),
)


def load_settings_group_fixture(group, fixture):
    model_group = Group(
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
                                type=setting[1].get('type'),
                                input=setting[1].get('input'),
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
        model_group = Group.objects.get(key=group)
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
    except Group.DoesNotExist:
        load_settings_group_fixture(group, fixture)


def load_settings_fixture(fixture):
    for group in fixture:
        load_settings_group_fixture(group[0], group[1])


def update_settings_fixture(fixture):
    for group in fixture:
        update_settings_group_fixture(group[0], group[1])


def load_fixtures():
    load_settings_fixture(settings_fixture)


def update_fixtures():
    update_settings_fixture(settings_fixture)
