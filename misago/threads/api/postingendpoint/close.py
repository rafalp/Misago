from rest_framework import serializers

from misago.threads import moderation

from . import PostingEndpoint, PostingMiddleware


class CloseMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.START

    def get_serializer(self):
        return CloseSerializer(data=self.request.data)

    def post_save(self, serializer):
        if self.thread.category.acl['can_close_threads']:
            if serializer.validated_data.get('close'):
                moderation.close_thread(self.request, self.thread)


class CloseSerializer(serializers.Serializer):
    close = serializers.BooleanField(required=False, default=False)
