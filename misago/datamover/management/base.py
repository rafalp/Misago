import time

from django.conf import settings
from django.core.management import base

from misago.datamover import OLD_FORUM


CommandError = base.CommandError


class BaseCommand(base.BaseCommand):
    def execute(self, *args, **options):
        self.check_move_setup()

        return super(BaseCommand, self).execute(*args, **options)

    def check_move_setup(self):
        if not 'misago05' in settings.DATABASES:
            raise CommandError(
                "You need to configure connection for your old database by "
                "adding \"misago05\" connection to your DATABASES"
            )

        if not OLD_FORUM:
            raise CommandError(
                "You need to configure migration from old forum by defining "
                "MISAGO_OLD_FORUM setting in your settings.py"
            )

    def start_timer(self):
        self._timer = time.time()

    def stop_timer(self):
        total_time = time.time() - self._timer
        return time.strftime('%H:%M:%S', time.gmtime(total_time))
