import random
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.template.defaultfilters import linebreaks_filter
from django.utils import timezone
from django.utils.six.moves import range

from faker import Factory
from misago.categories.models import Category
from misago.core.management.progressbar import show_progress
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Post, Thread


class Command(BaseCommand):
    help = 'Creates random threads and posts for dev and testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            'threads',
            help="number of threads to create",
            nargs='?',
            type=int,
            default=5
        )

    def handle(self, *args, **options):
        items_to_create = options['threads']

        categories = list(Category.objects.all_categories())

        fake = Factory.create()

        User = get_user_model()
        total_users = User.objects.count()

        self.stdout.write('Creating fake threads...\n')

        message = '\nSuccessfully created %s fake threads in %s'

        created_threads = 0
        start_time = time.time()
        show_progress(self, created_threads, items_to_create)

        while created_threads < items_to_create:
            with atomic():
                datetime = timezone.now()
                category = random.choice(categories)
                user = User.objects.order_by('?')[:1][0]

                thread_is_unapproved = random.randint(0, 100) > 90
                thread_is_hidden = random.randint(0, 100) > 90
                thread_is_closed = random.randint(0, 100) > 90

                thread = Thread(
                    category=category,
                    started_on=datetime,
                    starter_name='-',
                    starter_slug='-',
                    last_post_on=datetime,
                    last_poster_name='-',
                    last_poster_slug='-',
                    replies=0,
                    is_unapproved=thread_is_unapproved,
                    is_hidden=thread_is_hidden,
                    is_closed=thread_is_closed
                )
                thread.set_title(fake.sentence())
                thread.save()

                fake_message = "\n\n".join(fake.paragraphs())
                post = Post.objects.create(
                    category=category,
                    thread=thread,
                    poster=user,
                    poster_name=user.username,
                    poster_ip=fake.ipv4(),
                    original=fake_message,
                    parsed=linebreaks_filter(fake_message),
                    posted_on=datetime,
                    updated_on=datetime
                )
                update_post_checksum(post)
                post.save(update_fields=['checksum'])

                thread.set_first_post(post)
                thread.set_last_post(post)
                thread.save()

                user.threads += 1
                user.posts += 1
                user.save()

                thread_type = random.randint(0, 100)
                if thread_type > 95:
                    thread_replies = random.randint(200, 2500)
                elif thread_type > 50:
                    thread_replies = random.randint(5, 30)
                else:
                    thread_replies = random.randint(0, 10)

                for x in range(thread_replies):
                    datetime = timezone.now()
                    user = User.objects.order_by('?')[:1][0]
                    fake_message = "\n\n".join(fake.paragraphs())

                    is_unapproved = random.randint(0, 100) > 97

                    post = Post.objects.create(
                        category=category,
                        thread=thread,
                        poster=user,
                        poster_name=user.username,
                        poster_ip=fake.ipv4(),
                        original=fake_message,
                        parsed=linebreaks_filter(fake_message),
                        is_unapproved=is_unapproved,
                        posted_on=datetime,
                        updated_on=datetime
                    )

                    if not is_unapproved:
                        is_hidden = random.randint(0, 100) > 97
                    else:
                        is_hidden = False

                    if is_hidden:
                        post.is_hidden = True

                        if random.randint(0, 100) < 80:
                            user = User.objects.order_by('?')[:1][0]
                            post.hidden_by = user
                            post.hidden_by_name = user.username
                            post.hidden_by_slug = user.username
                        else:
                            post.hidden_by_name = fake.first_name()
                            post.hidden_by_slug = post.hidden_by_name.lower()

                    update_post_checksum(post)
                    post.save()

                    user.posts += 1
                    user.save()

                thread.synchronize()
                thread.save()

                created_threads += 1
                show_progress(
                    self, created_threads, items_to_create, start_time)

        pinned_threads = random.randint(0, int(created_threads * 0.025)) or 1
        self.stdout.write('\nPinning %s threads...' % pinned_threads)
        for i in range(0, pinned_threads):
            thread = Thread.objects.order_by('?')[:1][0]
            if random.randint(0, 100) > 75:
                thread.weight = 2
            else:
                thread.weight = 1
            thread.save()

        for category in categories:
            category.synchronize()
            category.save()

        total_time = time.time() - start_time
        total_humanized = time.strftime('%H:%M:%S', time.gmtime(total_time))
        self.stdout.write(message % (created_threads, total_humanized))
