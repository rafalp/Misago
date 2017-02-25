from __future__ import unicode_literals

import os

from django.contrib.auth import get_user_model
from django.core.files import File

from misago.threads.models import Attachment, AttachmentType, Post
from misago.threads.serializers import AttachmentSerializer

from . import OLD_FORUM, fetch_assoc, localise_datetime, movedids


UserModel = get_user_model()

IMAGE_TYPES = ('image/gif', 'image/jpeg', 'image/png', )


def move_attachments(stdout, style):
    query = 'SELECT * FROM misago_attachment ORDER BY id'

    posts = []

    attachment_types = {}
    for attachment_type in AttachmentType.objects.all():
        for mimetype in attachment_type.mimetypes_list:
            attachment_types[mimetype] = attachment_type

    for attachment in fetch_assoc(query):
        if attachment['content_type'] not in attachment_types:
            stdout.write(
                style.WARNING("Skipping attachment: %s (invalid type)" % attachment['name'])
            )
            continue

        if not attachment['post_id']:
            stdout.write(style.WARNING("Skipping attachment: %s (orphaned)" % attachment['name']))
            continue

        filetype = attachment_types[attachment['content_type']]

        post_pk = movedids.get('post', attachment['post_id'])
        post = Post.objects.get(pk=post_pk)

        if post_pk not in posts:
            posts.append(post_pk)

        uploader = None
        if attachment['user_id']:
            uploader_pk = movedids.get('user', attachment['user_id'])
            uploader = UserModel.objects.get(pk=uploader_pk)

        file_path = os.path.join(OLD_FORUM['ATTACHMENTS'], attachment['path'])
        upload = OldAttachmentFile(open(file_path, 'rb'), attachment)

        new_attachment = Attachment(
            secret=Attachment.generate_new_secret(),
            filetype=filetype,
            post=post,
            uploaded_on=localise_datetime(attachment['date']),
            uploader=uploader,
            uploader_name=attachment['user_name'],
            uploader_slug=attachment['user_name_slug'],
            uploader_ip=attachment['ip'],
            filename=attachment['name'],
            size=attachment['size'],
        )

        if attachment['content_type'] in IMAGE_TYPES:
            new_attachment.set_image(upload)
        else:
            new_attachment.set_file(upload)

        new_attachment.save()

        movedids.set('attachment', attachment['id'], new_attachment.pk)

    update_attachments_caches(posts)


def update_attachments_caches(posts):
    for post in Post.objects.filter(pk__in=posts).iterator():
        attachments = post.attachment_set.order_by('id')
        post.attachments_cache = AttachmentSerializer(attachments, many=True).data
        for attachment in post.attachments_cache:
            del attachment['acl']
            del attachment['post']
            del attachment['uploader_ip']
        post.save()


class OldAttachmentFile(File):
    def __init__(self, file, attachment):
        self._attachment = attachment
        self.name = attachment['name']

        self.file = file
        if hasattr(file, 'mode'):
            self.mode = file.mode
