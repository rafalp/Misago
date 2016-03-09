import random
import sys
import time

from django.core.management.base import BaseCommand
from faker import Factory

from misago.acl import version as acl_version
from misago.core.management.progressbar import show_progress

from misago.categories.models import Category, RoleCategoryACL


class Command(BaseCommand):
    help = 'Creates random fakey categories for testing purposes'

    def handle(self, *args, **options):
        try:
            fake_cats_to_create = int(args[0])
        except IndexError:
            fake_cats_to_create = 5
        except ValueError:
            self.stderr.write("\nOptional argument should be integer.")
            sys.exit(1)

        categories = Category.objects.all_categories(True)

        try:
            min_level = int(args[1])
        except (IndexError):
            min_level = 0
        except ValueError:
            self.stderr.write("\nSecond optional argument should be integer.")
            sys.exit(1)

        categories = categories.filter(level__gte=min_level)
        fake = Factory.create()

        message = 'Creating %s fake categories...\n'
        self.stdout.write(message % fake_cats_to_create)

        message = '\n\nSuccessfully created %s fake categories'

        created_count = 0
        start_time = time.time()
        show_progress(self, created_count, fake_cats_to_create)
        for i in xrange(fake_cats_to_create):
            parent = random.choice(categories)

            new_category = Category()
            if random.randint(1, 100) > 75:
                new_category.set_name(fake.catch_phrase().title())
            else:
                new_category.set_name(fake.street_name())

            if random.randint(1, 100) > 50:
                if random.randint(1, 100) > 80:
                    new_category.description = '\r\n'.join(fake.paragraphs())
                else:
                    new_category.description = fake.paragraph()

            new_category.insert_at(parent,
                position='last-child',
                save=True,
            )

            copied_acls = []
            copy_acl_from = random.choice(Category.objects.all_categories())
            for acl in copy_acl_from.category_role_set.all():
                copied_acls.append(RoleCategoryACL(
                    role_id=acl.role_id,
                    category=new_category,
                    category_role_id=acl.category_role_id,
                ))

            if copied_acls:
                acl_version.invalidate()
                RoleCategoryACL.objects.bulk_create(copied_acls)

            created_count += 1
            show_progress(
                self, created_count, fake_cats_to_create, start_time)

        self.stdout.write(message % created_count)
