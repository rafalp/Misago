import random
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.core.management.progressbar import show_progress


UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Adds random followers for testing purposes'

    def handle(self, *args, **options):
        total_users = UserModel.objects.count()

        message = 'Adding fake followers to %s users...\n'
        self.stdout.write(message % total_users)

        message = '\nSuccessfully added %s fake followers in %s'

        total_followers = 0
        processed_count = 0

        start_time = time.time()
        show_progress(self, processed_count, total_users)
        for user in UserModel.objects.iterator():
            user.followed_by.clear()

            if random.randint(1, 100) > 10:
                processed_count += 1
                show_progress(self, processed_count, total_users)
                continue  # 10% active users

            users_to_add = random.randint(1, total_users / 5)
            random_queryset = UserModel.objects.exclude(id=user.id).order_by('?')
            while users_to_add > 0:
                new_follower = random_queryset[:1][0]
                if not new_follower.is_following(user):
                    user.followed_by.add(new_follower)
                    users_to_add -= 1
                    total_followers += 1

            processed_count += 1
            show_progress(self, processed_count, total_users)

        self.stdout.write('\nSyncing models...')
        for user in UserModel.objects.iterator():
            user.followers = user.followed_by.count()
            user.following = user.follows.count()
            user.save(update_fields=['followers', 'following'])

        total_time = time.time() - start_time
        total_humanized = time.strftime('%H:%M:%S', time.gmtime(total_time))
        self.stdout.write(message % (total_followers, total_humanized))
