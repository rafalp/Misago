from rest_framework import serializers

from . import PostingEndpoint, PostingMiddleware
from ... import moderation


class HideMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.START

    def get_serializer(self):
        return HideSerializer(data=self.request.data)

    def post_save(self, serializer):
        if self.thread.category.acl["can_hide_threads"]:
            if serializer.validated_data.get("hide"):
                moderation.hide_thread(self.request, self.thread)
                self.thread.update_all = True
                self.thread.save(update_fields=["is_hidden"])

                self.thread.category.synchronize()
                self.thread.category.update_all = True


class HideSerializer(serializers.Serializer):
    hide = serializers.BooleanField(required=False, default=False)
