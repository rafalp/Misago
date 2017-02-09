from __future__ import unicode_literals

import re

from misago.datamover import fetch_assoc, movedids
from misago.threads.models import Attachment


ATTACHMENT_RE = re.compile(r'/attachment/(?P<hash>[a-z0-9]+)/')
ATTACHMENT_THUMB_RE = re.compile(r'/attachment/thumb/(?P<hash>[a-z0-9]+)/')


def update_attachments_urls(post):
    if '/attachment/' not in post:
        return post

    post = ATTACHMENT_THUMB_RE.sub(update_thumb_url, post)
    post = ATTACHMENT_RE.sub(update_full_url, post)

    return post


def update_thumb_url(matchobj):
    hash = matchobj.group('hash')
    attachment = get_attachment_for_hash(hash)
    if attachment:
        if attachment.thumbnail:
            return attachment.get_thumbnail_url()
        else:
            return attachment.get_absolute_url()
    return matchobj.group(0)


def update_full_url(matchobj):
    hash = matchobj.group('hash')
    attachment = get_attachment_for_hash(hash)
    if attachment:
        return attachment.get_absolute_url()
    return matchobj.group(0)


def get_attachment_for_hash(hash):
    query = 'SELECT * FROM misago_attachment WHERE hash_id = %s'
    for attachment in fetch_assoc(query, [hash]):
        attachment_pk = movedids.get('attachment', attachment['id'])
        try:
            return Attachment.objects.get(pk=attachment_pk)
        except Attachment.DoesNotExist:
            return None
    return None
