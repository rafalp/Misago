import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.core.management.progressbar import show_progress


class Command(BaseCommand):
    help = 'Adds random followers for testing purposes'

    def handle(self, *args, **options):
        User = get_user_model()
        total_users = User.objects.count()

        message = 'Adding fake followers to %s users...\n'
        self.stdout.write(message % total_users)

        message = '\nSuccessfully added %s fake followers'

        total_followers = 0
        processed_count = 0

        show_progress(self, processed_count, total_users)
        for user in User.objects.iterator():
            user.followed_by.clear()

            if random.randint(1, 100) > 10:
                processed_count += 1
                show_progress(self, processed_count, total_users)
                continue # 10% active users

            users_to_add = random.randint(1, total_users / 5)
            random_queryset = User.objects.exclude(id=user.id).order_by('?')
            while users_to_add > 0:
                new_follower = random_queryset[:1][0]
                if not new_follower.is_following(user):
                    user.followed_by.add(new_follower)
                    users_to_add -= 1
                    total_followers += 1

            processed_count += 1
            show_progress(self, processed_count, total_users)

        self.stdout.write('\nSyncing models...')
        for user in User.objects.iterator():
            user.followers = user.followed_by.count()
            user.following = user.follows.count()
            user.save(update_fields=['followers', 'following'])

        self.stdout.write(message % total_followers)
