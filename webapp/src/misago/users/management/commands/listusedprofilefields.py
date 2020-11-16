from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....core.pgutils import chunk_queryset

User = get_user_model()


class Command(BaseCommand):
    help = "Lists all profile fields in use."

    def handle(self, *args, **options):
        keys = {}

        for user in chunk_queryset(User.objects.all()):
            for key in user.profile_fields:
                keys.setdefault(key, 0)
                keys[key] += 1

        if keys:
            max_len = max([len(k) for k in keys])
            for key in sorted(keys):
                space = " " * (max_len + 1 - len(key))
                self.stdout.write("%s:%s%s" % (key, space, keys[key]))
        else:
            self.stdout.write("No profile fields are currently in use.")
