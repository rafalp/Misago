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
                'position':     0,
            }),
            ('board_header', {
                'type':         "string",
                'input':        "text",
                'name':         _("Board Header"),
                'description':  _("Some themes allow you to define text in board header. Leave empty to use Board Name instead."),
                'position':     1,
            }),
            ('board_header_postscript', {
                'value':        "Work in progress ",
                'type':         "string",
                'input':        "text",
                'name':         _("Board Header Postscript"),
                'description':  _("Additional text displayed in some themes board header after board name."),
                'position':     2,
            }),
            ('board_index_title', {
                'type':         "string",
                'input':        "text",
                'separator':    _("Board Index"),
                'name':         _("Board Index Title"),
                'description':  _("If you want to, you can replace page title content on Board Index with custom one."),
                'position':     3,
            }),
            ('board_index_meta', {
                'type':         "string",
                'input':        "text",
                'name':         _("Board Index Meta-Description"),
                'description':  _("Meta-Description used to describe your board's index page."),
                'position':     4,
            }),
            ('board_credits', {
                'type':         "string",
                'input':        "textarea",
                'separator':    _("Board Footer"),
                'name':         _("Custom Credit"),
                'description':  _("Custom Credit to display in board footer above software and theme copyright information. You can use HTML."),
                'position':     5,
            }),
            ('email_footnote', {
                'type':         "string",
                'input':        "textarea",
                'separator':    _("Board E-Mails"),
                'name':         _("Custom Footnote in HTML E-mails"),
                'description':  _("Custom Footnote to display in HTML e-mail messages sent by board."),
                'position':     6,
            }),
            ('email_footnote_plain', {
                'type':         "string",
                'input':        "textarea",
                'name':         _("Custom Footnote in plain text E-mails"),
                'description':  _("Custom Footnote to display in plain text e-mail messages sent by board."),
                'position':     7,
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
                                position=setting[1].get('position'),
                                separator=get_msgid(setting[1].get('separator')),
                                name=get_msgid(setting[1].get('name')),
                                description=get_msgid(setting[1].get('description')),
                            )
        model_setting.save(force_insert=True)


def update_settings_group_fixture(group, fixture):
    try:
        # Get and update group entry
        model_group = Group.objects.get(key=group)
        model_group.name = get_msgid(fixture['name'])
        model_group.description = get_msgid(fixture.get('description'))
        model_group.save(force_update=True)
        
        # Update group settings
        fixture = fixture.get('settings', ())
        for setting in fixture:
            # Clear setting value
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
            try:
                # Update setting entry
                model_setting = Setting.objects.get(setting=setting[0])
                model_setting.value_default = value_default
                model_setting.type = setting[1].get('type')
                model_setting.input = setting[1].get('input')
                model_setting.extra = base64.encodestring(pickle.dumps(setting[1].get('extra', {}), pickle.HIGHEST_PROTOCOL))
                model_setting.position = setting[1].get('position')
                model_setting.separator = get_msgid(setting[1].get('separator'))
                model_setting.name = get_msgid(setting[1].get('name'))
                model_setting.description = get_msgid(setting[1].get('description'))
                model_setting.save(force_update=True)
            except Setting.DoesNotExist:
                # Store setting in database
                model_setting = Setting(
                                        setting=setting[0],
                                        group=model_group,
                                        value=value,
                                        value_default=value_default,
                                        type=setting[1].get('type'),
                                        input=setting[1].get('input'),
                                        extra=base64.encodestring(pickle.dumps(setting[1].get('extra', {}), pickle.HIGHEST_PROTOCOL)),
                                        position=setting[1].get('position'),
                                        separator=get_msgid(setting[1].get('separator')),
                                        name=get_msgid(setting[1].get('name')),
                                        description=get_msgid(setting[1].get('description')),
                                    )
                model_setting.save(force_insert=True)
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