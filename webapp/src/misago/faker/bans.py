import random
from datetime import timedelta

from django.utils import timezone

from ..users.models import Ban


def get_fake_username_ban(fake):
    ban = _create_base_ban(fake, Ban.USERNAME)

    banned_value = fake.first_name()
    if random.randint(0, 100) < 31:
        banned_value = "%s*" % banned_value
    elif random.randint(0, 100) < 31:
        banned_value = "*%s" % banned_value
    elif random.randint(0, 100) < 31:
        banned_value = list(banned_value)
        banned_value.insert(random.randint(0, len(banned_value) - 1), "*")
        banned_value = "".join(banned_value)

    ban.banned_value = banned_value
    ban.save()
    return ban


def get_fake_email_ban(fake):
    ban = _create_base_ban(fake, Ban.EMAIL)

    if random.randint(0, 100) < 35:
        ban.banned_value = "*@%s" % fake.domain_name()
    else:
        ban.banned_value = fake.email()

    ban.save()
    return ban


def get_fake_ip_ban(fake):
    ban = _create_base_ban(fake, Ban.IP)

    if random.randint(0, 1):
        banned_value = fake.ipv4()
        if random.randint(0, 100) < 35:
            banned_value = banned_value.split(".")
            banned_value = ".".join(banned_value[: random.randint(1, 3)])
            banned_value = "%s.*" % banned_value
        elif random.randint(0, 100) < 35:
            banned_value = banned_value.split(".")
            banned_value = ".".join(banned_value[random.randint(1, 3) :])
            banned_value = "*.%s" % banned_value
        elif random.randint(0, 100) < 35:
            banned_value = banned_value.split(".")
            banned_value[random.randint(0, 3)] = "*"
            banned_value = ".".join(banned_value)
    else:
        banned_value = fake.ipv6()

        if random.randint(0, 100) < 35:
            banned_value = banned_value.split(":")
            banned_value = ":".join(banned_value[: random.randint(1, 7)])
            banned_value = "%s:*" % banned_value
        elif random.randint(0, 100) < 35:
            banned_value = banned_value.split(":")
            banned_value = ":".join(banned_value[: random.randint(1, 7)])
            banned_value = "*:%s" % banned_value
        elif random.randint(0, 100) < 35:
            banned_value = banned_value.split(":")
            banned_value[random.randint(0, 7)] = "*"
            banned_value = ":".join(banned_value)

    ban.banned_value = banned_value
    ban.save()
    return ban


def _create_base_ban(fake, ban_type):
    ban = Ban(check_type=ban_type)

    if random.randint(0, 10) == 0:
        ban.user_message = fake.sentence()

    if random.randint(0, 10) == 0:
        ban.staff_message = fake.sentence()

    if random.randint(0, 1):
        # Lets make ban temporary
        ban_length = timedelta(days=random.randint(0, 300))
        if random.randint(0, 1):
            ban.valid_until = timezone.now().date() - ban_length
        else:
            ban.valid_until = timezone.now().date() + ban_length

    return ban
