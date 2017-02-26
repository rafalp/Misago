from misago.core.pgutils import batch_update
from misago.datamover.management.base import BaseCommand
from misago.datamover.models import MovedId, OldIdRedirect


MAPPINGS = {
    'category': OldIdRedirect.CATEGORY,
    'post': OldIdRedirect.POST,
    'thread': OldIdRedirect.THREAD,
    'user': OldIdRedirect.USER,
}


class Command(BaseCommand):
    help = ("Builds moves index for redirects from old urls to new ones.")

    def handle(self, *args, **options):
        self.stdout.write("Building moves index...")

        counter = 1
        self.start_timer()

        for moved_id in batch_update(MovedId.objects):
            counter += 1

            if moved_id.model not in MAPPINGS:
                continue

            OldIdRedirect.objects.create(
                model=MAPPINGS[moved_id.model],
                old_id=moved_id.old_id,
                new_id=moved_id.new_id,
            )

        summary = "Indexed %s items in %s" % (counter, self.stop_timer())
        self.stdout.write(self.style.SUCCESS(summary))
