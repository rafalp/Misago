from __future__ import unicode_literals

from django.utils.crypto import get_random_string

from misago.core.pgutils import batch_update
from misago.markup import common_flavour
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Post

from .attachments import update_attachments_urls
from .quotes import convert_quotes_to_bbcode


def clean_posts():
    for post in batch_update(Post.objects):
        post.original = clean_original(post.original)

        parsed_post = common_flavour(FakeRequest(), FakeUser(), post.original)
        post.parsed = parsed_post['parsed_text']

        update_post_checksum(post)
        post.save()


def clean_original(post):
    post = convert_quotes_to_bbcode(post)
    post = update_attachments_urls(post)

    return post


"""
Fake request and user for parser
"""


class FakeUser(object):
    slug = get_random_string(40)


class FakeRequest(object):
    scheme = 'http'
    user = FakeUser()

    def get_host(self):
        return '{}.com'.format(get_random_string(40))
