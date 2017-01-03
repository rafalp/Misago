from ...models import MovedId, OldIdRedirect
from ..base import BaseCommand


MAPPINGS = {
    'attachment': 0,
    'category': 1,
    'post': 2,
    'thread': 3,
    'user': 4,
}


class Command(BaseCommand):
    help = (
        "Builds moves index for redirects from old urls to new ones."
    )

    def handle(self, *args, **options):
        self.stdout.write("Building moves index...")

        counter = 1
        self.start_timer()

        for moved_id in MovedId.objects.exclude(model='label').iterator():
            counter += 1
            OldIdRedirect.objects.create(
                model=MAPPINGS[moved_id.model],
                old_id=moved_id.old_id,
                new_id=moved_id.new_id,
            )

        summary = "Indexed %s items in %s" % (counter, self.stop_timer())
        self.stdout.write(self.style.SUCCESS(summary))
