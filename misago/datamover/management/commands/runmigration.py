from django.core.management import call_command

from misago.datamover.management.base import BaseCommand


MOVE_COMMANDS = [
    'movesettings',
    'moveusers',
    'movecategories',
    'movethreads',
    'buildmovesindex',
    'synchronizethreads',
    'synchronizecategories',
    'rebuildpostssearch',
    'invalidatebans',
    'populateonlinetracker',
    'synchronizeusers',
]


class Command(BaseCommand):
    help = ("Executes complete migration from Misago 0.5 together with cleanups.")

    def handle(self, *args, **options):
        self.stdout.write("Running complete migration...")

        self.start_timer()

        for command_to_call in MOVE_COMMANDS:
            call_command(command_to_call)

        summary = "Migration was completed in %s" % self.stop_timer()
        self.stdout.write(self.style.SUCCESS(summary))
