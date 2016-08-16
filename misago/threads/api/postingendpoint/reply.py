from django.db.models import F
from django.utils.translation import ugettext_lazy

from rest_framework import serializers

from misago.conf import settings
from misago.markup import common_flavour

from . import PostingEndpoint, PostingMiddleware
from ...checksums import update_post_checksum
from ...validators import validate_post, validate_title


class ReplyMiddleware(PostingMiddleware):
    def get_serializer(self):
        if self.mode == PostingEndpoint.START:
            return ThreadSerializer(data=self.request.data)
        else:
            return ReplySerializer(data=self.request.data)

    def save(self, serializer):
        if self.mode == PostingEndpoint.START:
            self.new_thread(serializer.validated_data)

        parsing_result = self.parse_post(serializer.validated_data['post'])

        if self.mode == PostingEndpoint.EDIT:
            self.edit_post(serializer.validated_data, parsing_result)
        else:
            self.new_post(serializer.validated_data, parsing_result)

        self.post.updated_on = self.datetime
        self.post.save()

        update_post_checksum(self.post)
        self.post.update_fields.append('checksum')

        if self.mode == PostingEndpoint.START:
            self.thread.set_first_post(self.post)
        if self.mode != PostingEndpoint.EDIT:
            self.thread.set_last_post(self.post)

        self.thread.save()

    def new_thread(self, validated_data):
        self.thread.set_title(validated_data['title'])
        self.thread.starter_name = self.user.username
        self.thread.starter_slug = self.user.slug
        self.thread.last_poster_name = self.user.username
        self.thread.last_poster_slug = self.user.slug
        self.thread.started_on = self.datetime
        self.thread.last_post_on = self.datetime
        self.thread.save()

    def edit_post(self, validated_data, parsing_result):
        self.post.original = parsing_result['original_text']
        self.post.parsed = parsing_result['parsed_text']

        self.post.updated_on = self.datetime
        self.post.edits = F('edits') + 1

        self.post.last_editor = self.user
        self.post.last_editor_name = self.user.username
        self.post.last_editor_slug = self.user.slug

    def new_post(self, validated_data, parsing_result):
        self.post.thread = self.thread
        self.post.poster = self.user
        self.post.poster_name = self.user.username
        self.post.poster_ip = self.request.user_ip
        self.post.posted_on = self.datetime

        self.post.original = parsing_result['original_text']
        self.post.parsed = parsing_result['parsed_text']

    def parse_post(self, post):
        if self.mode == PostingEndpoint.START:
            return common_flavour(self.request, self.user, post)
        else:
            return common_flavour(self.request, self.post.poster, post)


class ReplySerializer(serializers.Serializer):
    post = serializers.CharField(
        validators=[validate_post],
        error_messages={
            'required': ugettext_lazy("You have to enter a message.")
        }
    )


class ThreadSerializer(ReplySerializer):
    title = serializers.CharField(
        validators=[validate_title],
        error_messages={
        'required': ugettext_lazy("You have to enter thread title.")
        }
    )
