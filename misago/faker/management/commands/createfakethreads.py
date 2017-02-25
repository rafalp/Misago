from __future__ import unicode_literals

import random
import time

from faker import Factory

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.utils import timezone

from misago.categories.models import Category
from misago.core.management.progressbar import show_progress
from misago.faker.englishcorpus import EnglishCorpus
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Post, Thread


PLACEKITTEN_URL = 'https://placekitten.com/g/%s/%s'

UserModel = get_user_model()

corpus = EnglishCorpus()
corpus_short = EnglishCorpus(max_length=150)


class Command(BaseCommand):
    help = 'Creates random threads and posts for dev and testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            'threads',
            help="number of threads to create",
            nargs='?',
            type=int,
            default=5,
        )

    def handle(self, *args, **options):
        items_to_create = options['threads']

        categories = list(Category.objects.all_categories())

        fake = Factory.create()

        self.stdout.write('Creating fake threads...\n')

        message = '\nSuccessfully created %s fake threads in %s'

        created_threads = 0
        start_time = time.time()
        show_progress(self, created_threads, items_to_create)

        while created_threads < items_to_create:
            with atomic():
                datetime = timezone.now()
                category = random.choice(categories)
                user = UserModel.objects.order_by('?')[:1][0]

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
                    is_closed=thread_is_closed,
                )
                thread.set_title(corpus_short.random_choice())
                thread.save()

                original, parsed = self.fake_post_content()

                post = Post.objects.create(
                    category=category,
                    thread=thread,
                    poster=user,
                    poster_name=user.username,
                    poster_ip=fake.ipv4(),
                    original=original,
                    parsed=parsed,
                    posted_on=datetime,
                    updated_on=datetime,
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
                if thread_type > 98:
                    thread_replies = random.randint(200, 2500)
                elif thread_type > 50:
                    thread_replies = random.randint(5, 30)
                else:
                    thread_replies = random.randint(0, 10)

                for _ in range(thread_replies):
                    datetime = timezone.now()
                    user = UserModel.objects.order_by('?')[:1][0]

                    original, parsed = self.fake_post_content()

                    is_unapproved = random.randint(0, 100) > 97

                    post = Post.objects.create(
                        category=category,
                        thread=thread,
                        poster=user,
                        poster_name=user.username,
                        poster_ip=fake.ipv4(),
                        original=original,
                        parsed=parsed,
                        is_unapproved=is_unapproved,
                        posted_on=datetime,
                        updated_on=datetime,
                    )

                    if not is_unapproved:
                        is_hidden = random.randint(0, 100) > 97
                    else:
                        is_hidden = False

                    if is_hidden:
                        post.is_hidden = True

                        if random.randint(0, 100) < 80:
                            user = UserModel.objects.order_by('?')[:1][0]
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
                show_progress(self, created_threads, items_to_create, start_time)

        pinned_threads = random.randint(0, int(created_threads * 0.025)) or 1
        self.stdout.write('\nPinning %s threads...' % pinned_threads)
        for _ in range(0, pinned_threads):
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

    def fake_post_content(self):
        raw = []
        parsed = []

        if random.randint(0, 100) > 80:
            paragraphs_to_make = random.randint(1, 20)
        else:
            paragraphs_to_make = random.randint(1, 5)

        for _ in range(paragraphs_to_make):
            if random.randint(0, 100) > 95:
                cat_width = random.randint(1, 16) * random.choice([100, 90, 80])
                cat_height = random.randint(1, 12) * random.choice([100, 90, 80])

                cat_url = PLACEKITTEN_URL % (cat_width, cat_height)

                raw.append('!(%s)' % cat_url)
                parsed.append('<p><img src="%s" alt=""/></p>' % cat_url)
            else:
                if random.randint(0, 100) > 95:
                    sentences_to_make = random.randint(1, 20)
                else:
                    sentences_to_make = random.randint(1, 7)
                raw.append(' '.join(corpus.random_sentences(sentences_to_make)))
                parsed.append('<p>%s</p>' % raw[-1])

        return "\n\n".join(raw), "\n".join(parsed)
