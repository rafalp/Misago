from django.core.management.base import BaseCommand

from misago.acl import version as acl_version
from misago.categories.models import Category


class Command(BaseCommand):
    """
    This command rebuilds the thread category tree.
    It can be useful when the category hierarchy is corrupt due to modifying directly
    in the database causing MPTT's nested sets to not align correctly.
    A typical case is when injecting default data into the database from outside misago.
    """
    help = 'Rebuilds the thread category tree'

    def handle(self, *args, **options):
        root = Category.objects.root_category()
        Category.objects.partial_rebuild(root.tree_id)
        self.stdout.write("Categories tree has been rebuild.")

        Category.objects.clear_cache()
        acl_version.invalidate()
        self.stdout.write("Caches have been cleared.")
