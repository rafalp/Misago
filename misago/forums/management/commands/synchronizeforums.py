from django.core.management.base import BaseCommand

from misago.core.management.progressbar import show_progress

from misago.forums.models import Forum


class Command(BaseCommand):
    help = 'Synchronizes forums'

    def handle(self, *args, **options):
        forums_to_sync = Forum.objects.count()

        message = 'Synchronizing %s forums...\n'
        self.stdout.write(message % forums_to_sync)

        message = '\n\nSynchronized %s forums'

        synchronized_count = 0
        show_progress(self, synchronized_count, forums_to_sync)
        for forum in Forum.objects.iterator():
            forum.synchronize()
            forum.save()

            synchronized_count += 1
            show_progress(self, synchronized_count, forums_to_sync)

        self.stdout.write(message % synchronized_count)
