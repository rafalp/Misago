import random
import time

from django.core.management.base import BaseCommand
from faker import Factory

from ....acl.cache import clear_acl_cache
from ....categories.models import Category
from ....core.management.progressbar import show_progress
from ...categories import fake_category, fake_closed_category


class Command(BaseCommand):
    help = "Creates fake categories for dev and testing purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "categories",
            help="number of categories to create",
            nargs="?",
            type=int,
            default=5,
        )

        parser.add_argument(
            "minlevel",
            help="min. level of created categories",
            nargs="?",
            type=int,
            default=0,
        )

    def handle(self, *args, **options):  # pylint: disable=too-many-locals
        items_to_create = options["categories"]
        min_level = options["minlevel"]

        fake = Factory.create()

        categories = Category.objects.all_categories(include_root=True).filter(
            level__gte=min_level
        )
        acl_source = list(Category.objects.all_categories())[0]

        if not categories.exists():
            self.stdout.write("No valid parent categories exist.\n")
            return

        message = "Creating %s fake categories...\n"
        self.stdout.write(message % items_to_create)

        created_count = 0
        start_time = time.time()
        show_progress(self, created_count, items_to_create)

        while created_count < items_to_create:
            categories = (
                Category.objects.all_categories(include_root=True)
                .filter(level__gte=min_level)
                .order_by("?")
            )
            parent = random.choice(categories)

            if random.randint(0, 100) > 90:
                fake_closed_category(fake, parent, copy_acl_from=acl_source)
            else:
                fake_category(fake, parent, copy_acl_from=acl_source)

            created_count += 1
            show_progress(self, created_count, items_to_create, start_time)

        clear_acl_cache()

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\n\nSuccessfully created %s fake categories in %s"
        self.stdout.write(message % (created_count, total_humanized))
