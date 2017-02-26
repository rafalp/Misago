from __future__ import unicode_literals

from misago.conf import db_settings
from misago.conf.models import Setting

from . import fetch_assoc


def copy_value(setting):
    def closure(old_value):
        setting_obj = Setting.objects.get(setting=setting)
        setting_obj.value = old_value
        setting_obj.save()
        return setting_obj

    return closure


def map_value(setting, translation):
    def closure(old_value):
        setting_obj = Setting.objects.get(setting=setting)
        setting_obj.value = translation[old_value]
        setting_obj.save()
        return setting_obj

    return closure


def convert_allow_custom_avatars(old_value):
    setting_obj = Setting.objects.get(setting='allow_custom_avatars')
    setting_obj.value = 'upload' in old_value.split(',')
    setting_obj.save()
    return setting_obj


SETTING_CONVERTER = {
    'board_name': copy_value('forum_name'),
    'board_index_title': copy_value('forum_index_title'),
    'board_index_meta': copy_value('forum_index_meta_description'),
    'board_header': copy_value('forum_branding_text'),
    'email_footnote_plain': copy_value('email_footer'),
    'tos_title': copy_value('terms_of_service_title'),
    'tos_url': copy_value('terms_of_service_link'),
    'tos_content': copy_value('terms_of_service'),
    'board_credits': copy_value('forum_footnote'),
    'thread_name_min': copy_value('thread_title_length_min'),
    'thread_name_max': copy_value('thread_title_length_max'),
    'post_length_min': copy_value('post_length_min'),
    'account_activation': map_value(
        'account_activation', {
            'none': 'none',
            'user': 'user',
            'admin': 'admin',
            'block': 'closed',
        }
    ),
    'username_length_min': copy_value('username_length_min'),
    'username_length_max': copy_value('username_length_max'),
    'password_length': copy_value('password_length_min'),
    'avatars_types': convert_allow_custom_avatars,
    'default_avatar': copy_value('default_avatar'),
    'upload_limit': copy_value('avatar_upload_limit'),
    'subscribe_start': map_value('subscribe_start', {
        '0': 'no',
        '1': 'watch',
        '2': 'watch_email',
    }),
    'subscribe_reply': map_value('subscribe_reply', {
        '0': 'no',
        '1': 'watch',
        '2': 'watch_email',
    }),
    'bots_registration': map_value('captcha_type', {
        'no': 'no',
        'recaptcha': 're',
        'qa': 'qa',
    }),
    'recaptcha_public': copy_value('recaptcha_site_key'),
    'recaptcha_private': copy_value('recaptcha_secret_key'),
    'qa_test': copy_value('qa_question'),
    'qa_test_help': copy_value('qa_help_text'),
    'qa_test_answers': copy_value('qa_answers'),
}


def move_settings(stdout=None):
    for row in fetch_assoc('SELECT * FROM misago_setting'):
        setting_key = row['setting']
        if setting_key in SETTING_CONVERTER:
            convert_setting = SETTING_CONVERTER[setting_key]
            setting_obj = convert_setting(row['value'])
            stdout.write(setting_obj.name)
    db_settings.flush_cache()
