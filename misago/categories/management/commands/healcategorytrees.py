from django.core.management.base import BaseCommand

from ....acl.cache import clear_acl_cache
from ....cache.enums import CacheName
from ....cache.versions import invalidate_cache
from ...mptt import heal_category_trees


class Command(BaseCommand):
    """
    This command rebuilds the category trees in the database.

    It's useful when the MPTT data of one or more categories becomes invalid,
    either due to a bug or manual database manipulation.
    """

    help = "Heals the category trees in the database"

    def handle(self, *args, **options):
        heal_category_trees()
        self.stdout.write("Rebuild category trees in the database.")

        invalidate_cache(
            CacheName.CATEGORIES,
            CacheName.MODERATORS,
            CacheName.PERMISSIONS,
        )

        clear_acl_cache()
        self.stdout.write("Cleared caches associated with category trees.")
