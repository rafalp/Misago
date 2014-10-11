import random
import time

from faker import Factory

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.template.defaultfilters import linebreaks_filter
from django.utils import timezone

from misago.core.management.progressbar import show_progress
from misago.forums.models import Forum
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Thread, Post


class Command(BaseCommand):
    help = 'Adds random threads and posts for testing purposes'

    def handle(self, *args, **options):
        try:
            fake_threads_to_create = int(args[0])
        except IndexError:
            fake_threads_to_create = 5
        except ValueError:
            self.stderr.write("\nOptional argument should be integer.")
            sys.exit(1)

        forums = [f for f in Forum.objects.all_forums().filter(role='forum')]

        fake = Factory.create()

        User = get_user_model()
        total_users = User.objects.count()

        self.stdout.write('Creating fake threads...\n')

        message = '\nSuccessfully created %s fake threads'

        created_threads = 0
        start_time = time.time()
        show_progress(self, created_threads, fake_threads_to_create)
        for i in xrange(fake_threads_to_create):
            with atomic():
                datetime = timezone.now()
                forum = random.choice(forums)
                user = User.objects.order_by('?')[:1][0]

                thread_is_moderated = random.randint(0, 100) > 90
                thread_is_hidden = random.randint(0, 100) > 90
                thread_is_closed = random.randint(0, 100) > 90

                thread = Thread(
                    forum=forum,
                    started_on=datetime,
                    starter_name='-',
                    starter_slug='-',
                    last_post_on=datetime,
                    last_poster_name='-',
                    last_poster_slug='-',
                    replies=random.randint(0, 2000),
                    is_moderated=thread_is_moderated,
                    is_hidden=thread_is_hidden,
                    is_closed=thread_is_closed)
                thread.set_title(fake.sentence())
                thread.save()

                fake_message = "\n\n".join(fake.paragraphs())
                post = Post.objects.create(
                    forum=forum,
                    thread=thread,
                    poster=user,
                    poster_name=user.username,
                    poster_ip=fake.ipv4(),
                    original=fake_message,
                    parsed=linebreaks_filter(fake_message),
                    posted_on=datetime,
                    updated_on=datetime)
                update_post_checksum(post)
                post.save(update_fields=['checksum'])

                thread.set_first_post(post)
                thread.set_last_post(post)
                thread.save()

                forum.threads += 1
                forum.posts += 1
                forum.set_last_thread(thread)
                forum.save()

                user.threads += 1
                user.posts += 1
                user.save()

                created_threads += 1
                show_progress(
                    self, created_threads, fake_threads_to_create, start_time)

        pinned_threads = random.randint(0, int(created_threads * 0.025)) or 1
        self.stdout.write('\nPinning %s threads...' % pinned_threads)
        for i in xrange(0, pinned_threads):
            thread = Thread.objects.order_by('?')[:1][0]
            thread.is_pinned = True
            thread.save()

        self.stdout.write(message % created_threads)
