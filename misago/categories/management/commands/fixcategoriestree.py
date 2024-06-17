from django.core.management.base import BaseCommand

from ....acl.cache import clear_acl_cache
from ....cache.enums import CacheName
from ....cache.versions import invalidate_cache
from ...models import Category


class Command(BaseCommand):
    """
    This command rebuilds the thread category tree.
    It can be useful when the category hierarchy is corrupt due to modifying directly
    in the database causing MPTT's nested sets to not align correctly.
    A typical case is when injecting default data into the database from outside misago.
    """

    help = "Rebuilds the thread category tree"

    def handle(self, *args, **options):
        root = Category.objects.root_category()
        Category.objects.partial_rebuild(root.tree_id)
        self.stdout.write("Categories tree has been rebuild.")

        invalidate_cache(
            CacheName.CATEGORIES,
            CacheName.MODERATORS,
            CacheName.PERMISSIONS,
        )

        clear_acl_cache()
        self.stdout.write("Caches have been cleared.")
