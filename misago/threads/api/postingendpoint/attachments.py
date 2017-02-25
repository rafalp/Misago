from rest_framework import serializers

from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.acl import add_acl
from misago.conf import settings
from misago.threads.serializers import AttachmentSerializer

from . import PostingEndpoint, PostingMiddleware


class AttachmentsMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return bool(self.user.acl_cache['max_attachment_size'])

    def get_serializer(self):
        return AttachmentsSerializer(
            data=self.request.data,
            context={
                'mode': self.mode,
                'user': self.user,
                'post': self.post,
            }
        )

    def save(self, serializer):
        serializer.save()


class AttachmentsSerializer(serializers.Serializer):
    attachments = serializers.ListField(child=serializers.IntegerField(), required=False)

    def validate_attachments(self, ids):
        self.update_attachments = False
        self.removed_attachments = []
        self.final_attachments = []

        ids = list(set(ids))

        validate_attachments_count(ids)

        attachments = self.get_initial_attachments(
            self.context['mode'], self.context['user'], self.context['post']
        )
        new_attachments = self.get_new_attachments(self.context['user'], ids)

        if not attachments and not new_attachments:
            return []  # no attachments

        # clean existing attachments
        for attachment in attachments:
            if attachment.pk in ids:
                self.final_attachments.append(attachment)
            else:
                if attachment.acl['can_delete']:
                    self.update_attachments = True
                    self.removed_attachments.append(attachment)
                else:
                    message = _(
                        "You don't have permission to remove \"%(attachment)s\" attachment."
                    )
                    raise serializers.ValidationError(
                        message % {'attachment': attachment.filename}
                    )

        if new_attachments:
            self.update_attachments = True
            self.final_attachments += new_attachments
            self.final_attachments.sort(key=lambda a: a.pk, reverse=True)

    def get_initial_attachments(self, mode, user, post):
        attachments = []
        if mode == PostingEndpoint.EDIT:
            queryset = post.attachment_set.select_related('filetype')
            attachments = list(queryset)
            add_acl(user, attachments)
        return attachments

    def get_new_attachments(self, user, ids):
        if not ids:
            return []

        queryset = user.attachment_set.select_related('filetype').filter(
            post__isnull=True,
            id__in=ids,
        )

        return list(queryset)

    def save(self):
        if not self.update_attachments:
            return

        if self.removed_attachments:
            for attachment in self.removed_attachments:
                attachment.delete_files()

            self.context['post'].attachment_set.filter(
                id__in=[a.id for a in self.removed_attachments]
            ).delete()

        if self.final_attachments:
            # sort final attachments by id, descending
            self.final_attachments.sort(key=lambda a: a.pk, reverse=True)
            self.context['user'].attachment_set.filter(
                id__in=[a.id for a in self.final_attachments]
            ).update(post=self.context['post'])

        self.sync_attachments_cache(self.context['post'], self.final_attachments)

    def sync_attachments_cache(self, post, attachments):
        if attachments:
            post.attachments_cache = AttachmentSerializer(attachments, many=True).data
            for attachment in post.attachments_cache:
                del attachment['acl']
                del attachment['post']
                del attachment['uploader_ip']
        else:
            post.attachments_cache = None
        post.update_fields.append('attachments_cache')


def validate_attachments_count(data):
    total_attachments = len(data)
    if total_attachments > settings.MISAGO_POST_ATTACHMENTS_LIMIT:
        message = ungettext(
            "You can't attach more than %(limit_value)s file to single post (added %(show_value)s).",
            "You can't attach more than %(limit_value)s flies to single post (added %(show_value)s).",
            settings.MISAGO_POST_ATTACHMENTS_LIMIT,
        )
        raise serializers.ValidationError(
            message % {
                'limit_value': settings.MISAGO_POST_ATTACHMENTS_LIMIT,
                'show_value': total_attachments,
            }
        )
