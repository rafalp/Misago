from rest_framework.response import Response

from ...moderation import posts as moderation
from ...permissions import (
    allow_delete_best_answer,
    allow_delete_event,
    allow_delete_post,
)
from ...serializers import DeletePostsSerializer


def delete_post(request, thread, post):
    if post.is_event:
        allow_delete_event(request.user_acl, post)
    else:
        allow_delete_best_answer(request.user_acl, post)
        allow_delete_post(request.user_acl, post)

    moderation.delete_post(request.user, post)

    sync_related(thread)
    return Response({})


def delete_bulk(request, thread):
    serializer = DeletePostsSerializer(
        data={"posts": request.data},
        context={
            "settings": request.settings,
            "thread": thread,
            "user_acl": request.user_acl,
        },
    )

    if not serializer.is_valid():
        if "posts" in serializer.errors:
            errors = serializer.errors["posts"]
        else:
            errors = list(serializer.errors.values())[0]
        # Fix for KeyError - errors[0]
        try:
            errors = errors[0]
        except KeyError:
            if errors and isinstance(errors, dict):
                errors = list(errors.values())[0][0]
        return Response({"detail": errors}, status=400)

    for post in serializer.validated_data["posts"]:
        post.delete()

    sync_related(thread)

    return Response({})


def sync_related(thread):
    thread.synchronize()
    thread.save()

    thread.category.synchronize()
    thread.category.save()
