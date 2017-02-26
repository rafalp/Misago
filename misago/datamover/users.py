from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from misago.users.models import UsernameChange
from misago.users.signatures import make_signature_checksum

from . import fetch_assoc, localise_datetime, movedids


UserModel = get_user_model()

PRIVATE_THREAD_INVITES = {
    0: 0,
    1: 0,
    2: 1,
    3: 2,
}


def move_users(stdout, style):
    existing_users = get_existing_users()

    for user in fetch_assoc('SELECT * FROM misago_user ORDER BY id'):
        if user['email'].lower() in existing_users:
            user_new_pk = existing_users[user['email'].lower()]
            new_user = UserModel.objects.get(pk=user_new_pk)
        else:
            try:
                new_user = UserModel.objects.create_user(
                    user['username'], user['email'], 'Pass.123'
                )
            except ValidationError:
                new_name = ''.join([user['username'][:10], get_random_string(4)])
                new_user = UserModel.objects.create_user(new_name, user['email'], 'Pass.123')

                formats = (user['username'], new_name)
                stdout.write(style.ERROR('"%s" has been registered as "%s"' % formats))

            new_user.password = user['password']

        new_user.joined_on = localise_datetime(user['join_date'])
        new_user.joined_from_ip = user['join_ip']

        new_user.last_login = localise_datetime(user['last_date'])
        new_user.last_ip = user['last_ip']

        new_user.is_hiding_presence = bool(user['hide_activity'])
        new_user.title = user['title'] or None

        new_user.requires_activation = user['activation']
        if new_user.requires_activation > 2:
            new_user.requires_activation = 1

        new_user.is_avatar_locked = user['avatar_ban']
        new_user.avatar_lock_user_message = user['avatar_ban_reason_user'] or None
        new_user.avatar_lock_staff_message = user['avatar_ban_reason_admin'] or None

        if user['signature'] and user['signature_preparsed']:
            new_user.signature = user['signature']
            new_user.signature_parsed = user['signature_preparsed']
            new_user.signature_checksum = make_signature_checksum(
                user['signature_preparsed'], new_user
            )

        new_user.is_signature_locked = user['signature_ban']
        new_user.signature_lock_user_message = user['signature_ban_reason_user'] or None
        new_user.signature_lock_staff_message = user['signature_ban_reason_admin'] or None

        new_user.limits_private_thread_invites_to = PRIVATE_THREAD_INVITES[user['allow_pds']]

        new_user.subscribe_to_started_threads = int(user['subscribe_start'])
        new_user.subscribe_to_replied_threads = int(user['subscribe_reply'])

        new_user.save()
        movedids.set('user', user['id'], new_user.pk)


def get_existing_users():
    existing_users = {}

    queryset = UserModel.objects.values_list('id', 'email')
    for pk, email in queryset.iterator():
        existing_users[email.lower()] = pk
    return existing_users


def move_followers():
    for follow in fetch_assoc('SELECT * FROM misago_user_follows ORDER BY id'):
        from_user_id = movedids.get('user', follow['from_user_id'])
        to_user_id = movedids.get('user', follow['to_user_id'])

        from_user = UserModel.objects.get(pk=from_user_id)
        to_user = UserModel.objects.get(pk=to_user_id)

        from_user.follows.add(to_user)


def move_blocks():
    for follow in fetch_assoc('SELECT * FROM misago_user_ignores ORDER BY id'):
        from_user_id = movedids.get('user', follow['from_user_id'])
        to_user_id = movedids.get('user', follow['to_user_id'])

        from_user = UserModel.objects.get(pk=from_user_id)
        to_user = UserModel.objects.get(pk=to_user_id)

        from_user.blocks.add(to_user)


def move_namehistory():
    query = 'SELECT DISTINCT user_id FROM misago_usernamechange ORDER BY user_id'
    for user in fetch_assoc(query):
        new_id = movedids.get('user', user['user_id'])
        new_user = UserModel.objects.get(pk=new_id)
        move_users_namehistory(new_user, user['user_id'])


def move_users_namehistory(user, old_id):
    username_history = []
    query = 'SELECT * FROM misago_usernamechange WHERE user_id = %s ORDER BY id'
    for namechange in fetch_assoc(query, [old_id]):
        if username_history:
            username_history[-1].new_username = namechange['old_username']

        username_history.append(
            UsernameChange(
                user=user,
                changed_by=user,
                changed_by_username=user.username,
                changed_on=localise_datetime(namechange['date']),
                new_username=user.username,
                old_username=namechange['old_username']
            )
        )

    UsernameChange.objects.bulk_create(username_history)
