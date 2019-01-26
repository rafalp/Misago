from django.utils import timezone

from ..threads.models import Thread
from .englishcorpus import EnglishCorpus
from .posts import get_fake_hidden_post, get_fake_post, get_fake_unapproved_post

corpus_short = EnglishCorpus(max_length=150)


def get_fake_thread(fake, category, starter):
    thread = create_fake_thread(fake, category, starter)
    thread.first_post = get_fake_post(fake, thread, starter)
    thread.save(update_fields=["first_post"])
    return thread


def get_fake_closed_thread(fake, category, starter):
    thread = get_fake_thread(fake, category, starter)
    thread.is_closed = True
    thread.save(update_fields=["is_closed"])
    return thread


def get_fake_hidden_thread(fake, category, starter, hidden_by=None):
    thread = create_fake_thread(fake, category, starter)
    thread.first_post = get_fake_hidden_post(fake, thread, starter, hidden_by)
    thread.save(update_fields=["first_post"])
    return thread


def get_fake_unapproved_thread(fake, category, starter):
    thread = create_fake_thread(fake, category, starter)
    thread.first_post = get_fake_unapproved_post(fake, thread, starter)
    thread.save(update_fields=["first_post"])
    return thread


def create_fake_thread(fake, category, starter):
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
    thread.set_title(corpus_short.random_sentence())
    thread.save()

    return thread
