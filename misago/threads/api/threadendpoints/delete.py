from django.db import transaction
from rest_framework.response import Response

from ...moderation import threads as moderation
from ...permissions import allow_delete_thread
from ...serializers import DeleteThreadsSerializer


@transaction.atomic
def delete_thread(request, thread):
    allow_delete_thread(request.user_acl, thread)
    moderation.delete_thread(request.user, thread)
    return Response({})


def delete_bulk(request, viewmodel):
    serializer = DeleteThreadsSerializer(
        data={"threads": request.data},
        context={"request": request, "viewmodel": viewmodel},
    )

    if not serializer.is_valid():
        if "threads" in serializer.errors:
            errors = serializer.errors["threads"]
            if "details" in errors:
                return Response(hydrate_error_details(errors["details"]), status=400)
            return Response({"detail": errors[0]}, status=403)

        errors = list(serializer.errors)[0][0]
        return Response({"detail": errors}, status=400)

    for thread in serializer.validated_data["threads"]:
        with transaction.atomic():
            delete_thread(request, thread)

    return Response([])


def hydrate_error_details(errors):
    for error in errors:
        error["thread"]["id"] = int(error["thread"]["id"])
    return errors
