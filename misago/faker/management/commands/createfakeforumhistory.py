import random
import time
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Factory

from ....categories.models import Category
from ....threads.checksums import update_post_checksum
from ....threads.models import Post, Thread
from ....users.models import Rank
from ...englishcorpus import EnglishCorpus
from ...users import (
    get_fake_inactive_user,
    get_fake_admin_activated_user,
    get_fake_banned_user,
    get_fake_user,
)

User = get_user_model()

corpus = EnglishCorpus()
corpus_short = EnglishCorpus(max_length=150)

USER = 0
THREAD = 1
POST = 2
ACTIONS = [USER, THREAD, POST, POST, POST]


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

    def handle(self, *args, **options):
        history_length = options["length"]
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
            for date_variation in get_random_date_variations(date, 0, 20):
                action = random.choice(ACTIONS)
                if action == USER:
                    self.create_fake_user(fake, date_variation, ranks)
                elif action == THREAD:
                    self.create_fake_thread(fake, date_variation, categories)
                elif action == POST:
                    self.create_fake_post(fake, date_variation)

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
        # There's 40% chance user has registered on this day
        if random.randint(1, 100) > 25:
            return

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

        # User is active
        else:
            user = get_fake_user(fake, rank)

        user.joined_on = date
        user.save(update_fields=["joined_on"])
        user.audittrail_set.all().delete()

        self.write_event(date, "%s has joined" % user)

    def create_fake_thread(self, fake, date, categories):
        user = self.get_random_user(date)
        category = random.choice(categories)

        thread_is_unapproved = random.randint(0, 100) > 90
        thread_is_hidden = random.randint(0, 100) > 90
        thread_is_closed = random.randint(0, 100) > 90

        thread = Thread(
            category=category,
            started_on=datetime,
            starter_name="-",
            starter_slug="-",
            last_post_on=datetime,
            last_poster_name="-",
            last_poster_slug="-",
            replies=0,
            is_unapproved=thread_is_unapproved,
            is_hidden=thread_is_hidden,
            is_closed=thread_is_closed,
        )
        thread.set_title(corpus_short.random_sentence())
        thread.save()

        self.write_event(date, '%s has started "%s" thread' % (user, "TODO"))

    def create_fake_post(self, fake, date):
        user = self.get_random_user(date)
        self.write_event(date, '%s has replied to "%s" thread' % (user, "TODO"))

    def get_random_user(self, date):
        return User.objects.filter(joined_on__lt=date).order_by("?").first()

    def write_event(self, date, event):
        formatted_date = date.strftime("%Y-%m-%d %H:%M")
        self.stdout.write("%s: %s" % (formatted_date, event))


def get_random_date_variations(date, min, max):
    variations = []
    for _ in range(random.randint(min, max)):
        random_offset = timedelta(minutes=random.randint(1, 1200))
        variations.append(date - random_offset)
    return sorted(variations)
