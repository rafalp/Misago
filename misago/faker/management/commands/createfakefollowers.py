import random
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....core.management.progressbar import show_progress

User = get_user_model()


class Command(BaseCommand):
    help = "Adds random followers for testing purposes"

    def handle(self, *args, **options):
        total_users = User.objects.count()
        if total_users < 2:
            self.stderr.write(
                "At least two users must exist in the databse in order for "
                "fake followers creation to be possible.\n"
            )
            return

        message = "Adding fake followers to %s users...\n"
        self.stdout.write(message % total_users)

        total_followers = 0
        processed_count = 0

        start_time = time.time()
        show_progress(self, processed_count, total_users)
        for user in User.objects.iterator():
            user.followed_by.clear()
            followers_to_create = random.randint(0, total_users - 1)
            while followers_to_create:
                # There's 34% chance we'll skip follower creation
                if random.randint(0, 100) > 34:
                    new_follower = (
                        User.objects.exclude(pk=user.pk).order_by("?")[:1].first()
                    )
                    if not user.is_following(new_follower):
                        user.follows.add(new_follower)
                followers_to_create -= 1

            processed_count += 1
            show_progress(self, processed_count, total_users)

        self.stdout.write("\nSynchronizing users...")
        for user in User.objects.iterator():
            user.followers = user.followed_by.count()
            user.following = user.follows.count()
            user.save(update_fields=["followers", "following"])

        total_time = time.time() - start_time
        total_humanized = time.strftime("%H:%M:%S", time.gmtime(total_time))
        message = "\nSuccessfully added %s fake followers in %s"
        self.stdout.write(message % (total_followers, total_humanized))
