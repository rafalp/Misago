from rest_framework import serializers

from . import PostingEndpoint, PostingMiddleware


class ProtectMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.EDIT

    def get_serializer(self):
        return ProtectSerializer(data=self.request.data)

    def post_save(self, serializer):
        if self.thread.category.acl["can_protect_posts"]:
            try:
                self.post.is_protected = serializer.validated_data.get("protect", False)
                self.post.update_fields.append("is_protected")
            except (TypeError, ValueError):
                pass


class ProtectSerializer(serializers.Serializer):
    protect = serializers.BooleanField(required=False, default=False)
