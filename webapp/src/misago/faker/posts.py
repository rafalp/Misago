import random

from django.utils import timezone

from ..threads.checksums import update_post_checksum
from ..threads.models import Post
from .englishcorpus import EnglishCorpus
from .users import get_fake_username

PLACEKITTEN_URL = "https://placekitten.com/g/%s/%s"

corpus = EnglishCorpus()


def get_fake_post(fake, thread, poster=None):
    original, parsed = get_fake_post_content(fake)
    posted_on = timezone.now()

    post = Post.objects.create(
        category=thread.category,
        thread=thread,
        poster=poster,
        poster_name=poster.username if poster else get_fake_username(fake),
        original=original,
        parsed=parsed,
        posted_on=posted_on,
        updated_on=posted_on,
    )
    update_post_checksum(post)
    post.save(update_fields=["checksum"])

    return post


def get_fake_unapproved_post(fake, thread, poster=None):
    post = get_fake_post(fake, thread, poster)
    post.is_unapproved = True
    post.save(update_fields=["is_unapproved"])
    return post


def get_fake_hidden_post(fake, thread, poster=None, hidden_by=None):
    post = get_fake_post(fake, thread, poster)
    post.is_hidden = True

    if hidden_by:
        post.hidden_by = hidden_by
        post.hidden_by_name = hidden_by.username
        post.hidden_by_slug = hidden_by.slug
    else:
        post.hidden_by_name = fake.first_name()
        post.hidden_by_slug = post.hidden_by_name.lower()

    post.save(
        update_fields=["is_unapproved", "hidden_by", "hidden_by_name", "hidden_by_slug"]
    )

    return post


def get_fake_post_content(fake):
    raw = []
    parsed = []

    if random.randint(0, 100) > 90:
        paragraphs_to_make = random.randint(1, 20)
    else:
        paragraphs_to_make = random.randint(1, 5)

    for _ in range(paragraphs_to_make):
        if random.randint(0, 100) > 95:
            cat_width = random.randint(1, 16) * random.choice([100, 90, 80])
            cat_height = random.randint(1, 12) * random.choice([100, 90, 80])

            cat_url = PLACEKITTEN_URL % (cat_width, cat_height)

            raw.append("!(%s)" % cat_url)
            parsed.append('<p><img src="%s" alt=""/></p>' % cat_url)
        else:
            if random.randint(0, 100) > 95:
                sentences_to_make = random.randint(1, 20)
            else:
                sentences_to_make = random.randint(1, 7)
            raw.append(" ".join(corpus.random_sentences(sentences_to_make)))
            parsed.append("<p>%s</p>" % raw[-1])

    return "\n\n".join(raw), "\n".join(parsed)
