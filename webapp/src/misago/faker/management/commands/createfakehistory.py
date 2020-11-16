import random
import time
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Factory

from ....categories.models import Category
from ....core.pgutils import chunk_queryset
from ....threads.checksums import update_post_checksum
from ....threads.models import Thread
from ....users.models import Rank
from ...posts import get_fake_hidden_post, get_fake_post, get_fake_unapproved_post
from ...threads import (
    get_fake_closed_thread,
    get_fake_hidden_thread,
    get_fake_thread,
    get_fake_unapproved_thread,
)
from ...users import (
    get_fake_admin_activated_user,
    get_fake_banned_user,
    get_fake_deleted_user,
    get_fake_inactive_user,
    get_fake_user,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Creates fake forum history reaching specified period."

    def add_arguments(self, parser):
        parser.add_argument(
            "length",
            help="generated history length (in days)",
            nargs="?",
            type=int,
            default=5,
        )
        parser.add_argument(
            "max_actions",
            help="number of items generate for a single day",
            nargs="?",
            type=int,
            default=50,
        )

    def handle(self, *args, **options):  # pylint: disable=too-many-locals
        history_length = options["length"]
        max_actions = options["max_actions"]
        fake = Factory.create()

        categories = list(Category.objects.all_categories())
        ranks = list(Rank.objects.all())

        message = "Creating fake forum history for %s days...\n"
        self.stdout.write(message % history_length)

        start_time = time.time()

        self.move_existing_users_to_past(history_length)

        start_timestamp = timezone.now()
        for days_ago in reversed(range(history_length)):
            date = start_timestamp - timedelta(days=days_ago)
            for date_variation in get_random_date_variations(date, 0, max_actions):
                action = random.randint(0, 100)
                if action >= 80:
                    self.create_fake_user(fake, date_variation, ranks)
                elif action > 50:
                    self.create_fake_thread(fake, date_variation, categories)
                else:
                    self.create_fake_post(fake, date_variation)

                if random.randint(0, 100) > 80:
                    self.create_fake_follow(date)

        self.synchronize_threads()
        self.synchronize_categories()

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\n\nSuccessfully created fake history for %s days in %s"
        self.stdout.write(message % (history_length, total_humanized))

    def move_existing_users_to_past(self, history_length):
        for user in User.objects.all():
            user.joined_on -= timedelta(days=history_length)
            user.save(update_fields=["joined_on"])
            user.audittrail_set.all().delete()

    def create_fake_user(self, fake, date, ranks):
        # Pick random rank for next user
        rank = random.choice(ranks)

        # There's 10% chance user is inactive
        if random.randint(0, 100) > 90:
            user = get_fake_inactive_user(fake, rank)

        # There's another 10% chance user is admin-activated
        elif random.randint(0, 100) > 90:
            user = get_fake_admin_activated_user(fake, rank)

        # And further chance user is banned
        elif random.randint(0, 100) > 90:
            user = get_fake_banned_user(fake, rank)

        # Or deleted their account
        elif random.randint(0, 100) > 90:
            user = get_fake_deleted_user(fake, rank)

        # User is active
        else:
            user = get_fake_user(fake, rank)

        user.joined_on = date
        user.save(update_fields=["joined_on"])
        user.audittrail_set.all().delete()

        self.write_event(date, "%s has joined" % user)

    def create_fake_thread(self, fake, date, categories):
        category = random.choice(categories)

        # 10% chance thread poster is anonymous
        if random.randint(0, 100) > 90:
            starter = None
        else:
            starter = self.get_random_user(date)

        # There's 10% chance thread is closed
        if random.randint(0, 100) > 90:
            thread = get_fake_closed_thread(fake, category, starter)

        # There's further 5% chance thread is hidden
        elif random.randint(0, 100) > 95:
            if random.randint(0, 100) > 90:
                hidden_by = None
            else:
                hidden_by = self.get_random_user(date)

            thread = get_fake_hidden_thread(fake, category, starter, hidden_by)

        # And further 5% chance thread is unapproved
        elif random.randint(0, 100) > 95:
            thread = get_fake_unapproved_thread(fake, category, starter)

        # Default, standard thread
        else:
            thread = get_fake_thread(fake, category, starter)

        thread.first_post.posted_on = date
        thread.first_post.updated_on = date
        thread.first_post.checksum = update_post_checksum(thread.first_post)
        thread.first_post.save(update_fields=["checksum", "posted_on", "updated_on"])

        thread.started_on = date
        thread.save(update_fields=["started_on"])

        self.write_event(
            date, '%s has started "%s" thread' % (thread.first_post.poster_name, thread)
        )

    def create_fake_post(self, fake, date):
        thread = self.get_random_thread(date)
        if not thread:
            return

        # 10% chance poster is anonymous
        if random.randint(0, 100) > 90:
            poster = None
        else:
            poster = self.get_random_user(date)

        # There's 5% chance post is unapproved
        if random.randint(0, 100) > 90:
            post = get_fake_unapproved_post(fake, thread, poster)

        # There's further 5% chance post is hidden
        elif random.randint(0, 100) > 95:
            if random.randint(0, 100) > 90:
                hidden_by = None
            else:
                hidden_by = self.get_random_user(date)

            post = get_fake_hidden_post(fake, thread, poster, hidden_by)

        # Default, standard post
        else:
            post = get_fake_post(fake, thread, poster)

        post.posted_on = date
        post.updated_on = date
        post.checksum = update_post_checksum(post)
        post.save(update_fields=["checksum", "posted_on", "updated_on"])

        self.write_event(
            date, '%s has replied to "%s" thread' % (post.poster_name, thread)
        )

    def create_fake_follow(self, date):
        user_a = self.get_random_user(date)
        user_b = self.get_random_user(date)

        if not (user_a or user_b) or user_a == user_b:
            return

        if not user_a.is_following(user_b):
            user_a.follows.add(user_b)

        self.write_event(date, "%s followed %s" % (user_a, user_b))

    def get_random_thread(self, date):
        return (
            Thread.objects.filter(started_on__lt=date)
            .select_related("category")
            .order_by("?")
            .first()
        )

    def get_random_user(self, date):
        return (
            User.objects.filter(
                joined_on__lt=date, requires_activation=User.ACTIVATION_NONE
            )
            .order_by("?")
            .first()
        )

    def write_event(self, date, event):
        formatted_date = date.strftime("%Y-%m-%d %H:%M")
        self.stdout.write("%s: %s" % (formatted_date, event))

    def synchronize_threads(self):
        self.stdout.write("\nSynchronizing threads...")
        start_time = time.time()

        for thread in chunk_queryset(Thread.objects.all()):
            thread.synchronize()
            thread.save()

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))

        message = "Synchronized %s threads in %s"
        self.stdout.write(message % (Thread.objects.count(), total_humanized))

    def synchronize_categories(self):
        self.stdout.write("\nSynchronizing categories...")
        start_time = time.time()

        for category in Category.objects.all_categories():
            category.synchronize()
            category.save()

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))

        message = "Synchronized %s categories in %s"
        self.stdout.write(message % (Category.objects.count(), total_humanized))


def get_random_date_variations(date, min_date, max_date):
    variations = []
    for _ in range(random.randint(min_date, max_date)):
        random_offset = timedelta(minutes=random.randint(1, 1200))
        variations.append(date - random_offset)
    return sorted(variations)
