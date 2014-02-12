from datetime import date
from time import time
import hashlib
import uuid
from path import path
from PIL import Image
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from floppyforms import ValidationError
from misago.signals import (delete_user_content, merge_post, merge_thread,
                            move_forum_content, move_post, move_thread,
                            rename_user, sync_user_profile)


class AttachmentManager(models.Manager):
    def allow_more_orphans(self):
        if Attachment.objects.filter(post__isnull=True).count() > settings.ORPHAN_ATTACHMENTS_LIMIT:
            raise ValidationError(_("Too many users are currently uploading files. Please try agian later."))


class Attachment(models.Model):
    hash_id = models.CharField(max_length=8, db_index=True)
    filetype = models.ForeignKey('AttachmentType')
    forum = models.ForeignKey('Forum', null=True, blank=True, on_delete=models.SET_NULL)
    thread = models.ForeignKey('Thread', null=True, blank=True, on_delete=models.SET_NULL)
    post = models.ForeignKey('Post', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255)
    user_name_slug = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    session = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    size = models.PositiveIntegerField(max_length=255)

    objects = AttachmentManager()

    class Meta:
        app_label = 'misago'

    def delete(self, *args, **kwargs):
        try:
            file_path = self.file_path
            if file_path.exists() and not file_path.isdir():
                file_path.unlink()
        except Exception:
            pass
        try:
            file_path = self.thumb_path
            if thumb_path.exists() and not thumb_path.isdir():
                thumb_path.unlink()
        except Exception:
            pass

        super(Attachment, self).delete(*args, **kwargs)

    def delete_from_post(self):
        if self.post_id:
            self.post.attachments = [attachment
                                     for attachment in self.post.attachments
                                     if attachment.pk != self.pk]
            self.post.save(force_update=True)

    @property
    def is_image(self):
        IMAGES_EXTENSIONS = ('.png', '.gif', '.jpg', '.jpeg')
        name = self.name.lower()

        for extension in IMAGES_EXTENSIONS:
            if name[len(extension) * -1:] == extension:
                return extension[1:]
        return False

    @property
    def file_path(self):
        return path(settings.ATTACHMENTS_ROOT + self.path)

    @property
    def thumb_path(self):
        return path(unicode(self.file_path).replace('.', '_thumb.'))

    def use_file(self, uploaded_file):
        self.name = self.clean_name(uploaded_file.name)
        self.content_type = uploaded_file.content_type
        self.size = uploaded_file.size

        self.store_file(uploaded_file)

    def clean_name(self, filename):
        for char in '=[]()<>\\/"\'':
            filename = filename.replace(char, '')
        if len(filename) > 100:
            filename = filename[-100:]
        return filename

    def store_file(self, uploaded_file):
        datenow = date.today()
        current_dir = '%s-%s-%s' % (datenow.month, datenow.day, datenow.year)

        full_dir = path(settings.ATTACHMENTS_ROOT + current_dir)
        full_dir.mkdir_p()

        filename = hashlib.md5('%s:%s:%s' % (self.user.pk, int(time()), settings.SECRET_KEY)).hexdigest()
        if self.is_image:
            filename += '.%s' % self.is_image
        self.path = '%s/%s' % (current_dir, filename)

        with open('%s/%s' % (full_dir, filename), 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        if self.is_image:
            self.make_thumb()

    def make_thumb(self):
        try:
            image = Image.open(self.file_path)
            image.thumbnail((800, 600), Image.ANTIALIAS)
            image.save(self.thumb_path)
        except IOError:
            pass

    def generate_hash_id(self, seed):
        hash_seed = '%s:%s' % (uuid.uuid4(), seed)
        unique_hash = hashlib.sha256(hash_seed).hexdigest()
        self.hash_id = unique_hash[:8]


def rename_user_handler(sender, **kwargs):
    sender.attachment_set.update(
                                 user_name=sender.username,
                                 user_name_slug=sender.username_slug,
                                )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_attachments")


def delete_user_content_handler(sender, **kwargs):
    for attachment in sender.attachment_set.iterator():
        if attachment.post_id:
            attachment.delete_from_post()
        attachment.delete()

delete_user_content.connect(delete_user_content_handler, dispatch_uid="delete_user_attachments")


def move_forum_content_handler(sender, **kwargs):
    sender.attachment_set.update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_attachments")


def move_thread_handler(sender, **kwargs):
    sender.attachment_set.update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_attachments")


def move_post_handler(sender, **kwargs):
    sender.attachment_set.update(forum=kwargs['move_to'].forum, thread=kwargs['move_to'])

move_post.connect(move_thread_handler, dispatch_uid="move_post_attachments")


def merge_thread_handler(sender, **kwargs):
    sender.attachment_set.update(thread=kwargs['new_thread'])

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_attachments")


def merge_post_handler(sender, **kwargs):
    sender.attachment_set.update(post=kwargs['new_post'], session=('attachments_%s' % kwargs['new_post'].pk))

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_posts_attachments")
