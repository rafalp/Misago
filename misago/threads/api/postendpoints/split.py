from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from rest_framework.response import Response

from ...models import Thread
from ...moderation import threads as moderation
from ...serializers import SplitPostsSerializer


def posts_split_endpoint(request, thread):
    if not thread.acl["can_move_posts"]:
        raise PermissionDenied(_("You can't split posts from this thread."))

    serializer = SplitPostsSerializer(
        data=request.data,
        context={
            "settings": request.settings,
            "thread": thread,
            "user_acl": request.user_acl,
        },
    )

    if not serializer.is_valid():
        if "posts" in serializer.errors:
            # Fix for KeyError - errors[0]
            errors = serializer.errors["posts"]
            try:
                errors = {"detail": errors[0]}
            except KeyError:
                if isinstance(errors, dict):
                    errors = {"detail": list(errors.values())[0][0]}
        else:
            errors = serializer.errors

        return Response(errors, status=400)

    split_posts_to_new_thread(request, thread, serializer.validated_data)

    return Response({})


def split_posts_to_new_thread(request, thread, validated_data):
    new_thread = Thread(
        category=validated_data["category"],
        started_on=thread.started_on,
        last_post_on=thread.last_post_on,
    )

    new_thread.set_title(validated_data["title"])
    new_thread.save()

    for post in validated_data["posts"]:
        post.move(new_thread)
        post.save()

    thread.synchronize()
    thread.save()

    new_thread.synchronize()
    new_thread.save()

    if validated_data.get("weight") == Thread.WEIGHT_GLOBAL:
        moderation.pin_thread_globally(request, new_thread)
    elif validated_data.get("weight"):
        moderation.pin_thread_locally(request, new_thread)
    if validated_data.get("is_hidden", False):
        moderation.hide_thread(request, new_thread)
    if validated_data.get("is_closed", False):
        moderation.close_thread(request, new_thread)

    thread.category.synchronize()
    thread.category.save()

    if new_thread.category != thread.category:
        new_thread.category.synchronize()
        new_thread.category.save()
