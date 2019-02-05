from django.utils import timezone

from ..threads.models import Thread
from .englishcorpus import EnglishCorpus
from .posts import get_fake_hidden_post, get_fake_post, get_fake_unapproved_post

corpus_short = EnglishCorpus(max_length=150)


def get_fake_thread(fake, category, starter=None):
    thread = _create_base_thread(fake, category)
    thread.first_post = get_fake_post(fake, thread, starter)
    thread.save(update_fields=["first_post"])
    return thread


def get_fake_closed_thread(fake, category, starter=None):
    thread = get_fake_thread(fake, category)
    thread.is_closed = True
    thread.save(update_fields=["is_closed"])
    return thread


def get_fake_hidden_thread(fake, category, starter=None, hidden_by=None):
    thread = _create_base_thread(fake, category)
    thread.first_post = get_fake_hidden_post(fake, thread, starter, hidden_by)
    thread.is_hidden = True
    thread.save(update_fields=["first_post", "is_hidden"])
    return thread


def get_fake_unapproved_thread(fake, category, starter=None):
    thread = _create_base_thread(fake, category)
    thread.first_post = get_fake_unapproved_post(fake, thread, starter)
    thread.is_unapproved = True
    thread.save(update_fields=["first_post", "is_unapproved"])
    return thread


def _create_base_thread(fake, category):
    started_on = timezone.now()
    thread = Thread(
        category=category,
        started_on=started_on,
        starter_name="-",
        starter_slug="-",
        last_post_on=started_on,
        last_poster_name="-",
        last_poster_slug="-",
        replies=0,
    )

    # Sometimes thread ends with slug being set to empty string
    while not thread.slug:
        thread.set_title(corpus_short.random_sentence())

    thread.save()

    return thread
