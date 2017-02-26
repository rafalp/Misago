from __future__ import unicode_literals

from misago.users.models import Ban

from . import fetch_assoc, localise_datetime


CHECK_MAPPING = {1: 0, 2: 1, 3: 2}


def move_bans():
    for ban in fetch_assoc('SELECT * FROM misago_ban'):
        if ban['test']:
            Ban.objects.create(
                check_type=CHECK_MAPPING[ban['test']],
                banned_value=ban['ban'],
                user_message=ban['reason_user'],
                staff_message=ban['reason_admin'],
                expires_on=localise_datetime(ban['expires']),
            )
        else:
            Ban.objects.create(
                check_type=0,
                banned_value=ban['ban'],
                user_message=ban['reason_user'],
                staff_message=ban['reason_admin'],
                expires_on=localise_datetime(ban['expires']),
            )

            Ban.objects.create(
                check_type=1,
                banned_value=ban['ban'],
                user_message=ban['reason_user'],
                staff_message=ban['reason_admin'],
                expires_on=localise_datetime(ban['expires']),
            )

    Ban.objects.invalidate_cache()
