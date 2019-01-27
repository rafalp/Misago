import random
import sys

from django.core.management.base import BaseCommand
from faker import Factory

from ....core.management.progressbar import show_progress
from ....users.models import Ban
from ...bans import get_fake_username_ban, get_fake_email_ban, get_fake_ip_ban


class Command(BaseCommand):
    help = "Creates random fakey bans for testing purposes"

    def handle(self, *args, **options):
        try:
            fake_bans_to_create = int(args[0])
        except IndexError:
            fake_bans_to_create = 5
        except ValueError:
            self.stderr.write("\nOptional argument should be integer.")
            sys.exit(1)

        fake = Factory.create()
        ban_fakers = (get_fake_username_ban, get_fake_email_ban, get_fake_ip_ban)

        message = "Creating %s fake bans...\n"
        self.stdout.write(message % fake_bans_to_create)

        created_count = 0
        show_progress(self, created_count, fake_bans_to_create)
        for _ in range(fake_bans_to_create):
            ban_faker = random.choice(ban_fakers)
            ban_faker(fake)

            created_count += 1
            show_progress(self, created_count, fake_bans_to_create)

        Ban.objects.invalidate_cache()

        message = "\n\nSuccessfully created %s fake bans"
        self.stdout.write(message % created_count)
