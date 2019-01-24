from django.utils import timezone

from ...englishcorpus import EnglishCorpus

PLACEKITTEN_URL = "https://placekitten.com/g/%s/%s"

corpus = EnglishCorpus()
corpus_short = EnglishCorpus(max_length=150)


def fake_thread(fake, category, starter):
    thread = Thread(
        category=category,
        started_on=timezone.now(),
        starter_name="-",
        starter_slug="-",
        last_post_on=timezone.now(),
        last_poster_name="-",
        last_poster_slug="-",
        replies=0,
    )
    thread.set_title(corpus_short.random_sentence())
    thread.save()

    return thread


def fake_closed_thread(fake, category, starter):
    thread = fake_thread(fake, category, starter)
    thread.is_closed = True
    thread.save(update_fields=["is_closed"])
    return thread


def fake_hidden_thread(fake, category, starter):
    thread = fake_thread(fake, category, starter)
    thread.is_hidden = True
    thread.save(update_fields=["is_hidden"])
    return thread


def fake_unapproved_thread(fake, category, starter):
    thread = fake_thread(fake, category, starter)
    thread.is_hidden = True
    thread.save(update_fields=["is_hidden"])
    return thread
