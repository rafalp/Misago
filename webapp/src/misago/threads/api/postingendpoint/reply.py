from django.utils.translation import gettext_lazy
from rest_framework import serializers

from . import PostingEndpoint, PostingMiddleware
from ....markup import common_flavour
from ....users.audittrail import create_audit_trail
from ...checksums import update_post_checksum
from ...validators import validate_post, validate_post_length, validate_thread_title


class ReplyMiddleware(PostingMiddleware):
    def get_serializer(self):
        if self.mode == PostingEndpoint.START:
            serializer = ThreadSerializer
        else:
            serializer = ReplySerializer

        return serializer(data=self.request.data, context=self.kwargs)

    def save(self, serializer):
        if self.mode == PostingEndpoint.START:
            self.new_thread(serializer.validated_data)

        parsing_result = serializer.validated_data["parsing_result"]

        if self.mode == PostingEndpoint.EDIT:
            self.edit_post(serializer.validated_data, parsing_result)
        else:
            self.new_post(serializer.validated_data, parsing_result)

        if self.mode == PostingEndpoint.START:
            self.post.set_search_document(self.thread.title)
        else:
            self.post.set_search_document()

        self.post.updated_on = self.datetime
        self.post.save()

        self.post.update_search_vector()
        update_post_checksum(self.post)

        self.post.update_fields += ["checksum", "search_vector"]

        if self.mode == PostingEndpoint.START:
            self.thread.set_first_post(self.post)
            self.thread.set_last_post(self.post)

        self.thread.save()

        create_audit_trail(self.request, self.post)

        # annotate post for future middlewares
        self.post.parsing_result = parsing_result

    def new_thread(self, validated_data):
        self.thread.set_title(validated_data["title"])
        self.thread.starter_name = self.user.username
        self.thread.starter_slug = self.user.slug
        self.thread.last_poster_name = self.user.username
        self.thread.last_poster_slug = self.user.slug
        self.thread.started_on = self.datetime
        self.thread.last_post_on = self.datetime
        self.thread.save()

    def edit_post(self, validated_data, parsing_result):
        self.post.original = parsing_result["original_text"]
        self.post.parsed = parsing_result["parsed_text"]

    def new_post(self, validated_data, parsing_result):
        self.post.thread = self.thread
        self.post.poster = self.user
        self.post.poster_name = self.user.username
        self.post.posted_on = self.datetime

        self.post.original = parsing_result["original_text"]
        self.post.parsed = parsing_result["parsed_text"]


class ReplySerializer(serializers.Serializer):
    post = serializers.CharField(
        error_messages={"required": gettext_lazy("You have to enter a message.")}
    )

    def validate_post(self, data):
        validate_post_length(self.context["settings"], data)
        return data

    def validate(self, data):
        if data.get("post"):
            data["parsing_result"] = self.parse_post(data["post"])
            data = validate_post(self.context, data)

        return data

    def parse_post(self, post):
        if self.context["mode"] == PostingEndpoint.START:
            return common_flavour(self.context["request"], self.context["user"], post)

        return common_flavour(
            self.context["request"], self.context["post"].poster, post
        )


class ThreadSerializer(ReplySerializer):
    title = serializers.CharField(
        error_messages={"required": gettext_lazy("You have to enter thread title.")}
    )

    def validate_title(self, data):
        validate_thread_title(self.context["settings"], data)
        return data
