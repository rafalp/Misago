from rest_framework import serializers

from misago.threads import moderation
from misago.threads.models import Thread

from . import PostingEndpoint, PostingMiddleware


class PinMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.START

    def get_serializer(self):
        return PinSerializer(data=self.request.data)

    def post_save(self, serializer):
        allowed_pin = self.thread.category.acl['can_pin_threads']
        if allowed_pin > 0:
            pin = serializer.validated_data['pin']

            if pin <= allowed_pin:
                if pin == Thread.WEIGHT_GLOBAL:
                    moderation.pin_thread_globally(self.request, self.thread)
                elif pin == Thread.WEIGHT_PINNED:
                    moderation.pin_thread_locally(self.request, self.thread)


class PinSerializer(serializers.Serializer):
    pin = serializers.IntegerField(required=False, default=0)
