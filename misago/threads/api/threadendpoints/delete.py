from rest_framework.response import Response

from django.db import transaction

from misago.threads import moderation
from misago.threads.permissions import allow_delete_thread
from misago.threads.serializers import DeleteThreadsSerializer



@transaction.atomic
def delete_thread(request, thread):
    allow_delete_thread(request.user, thread)
    moderation.delete_thread(request.user, thread)
    return Response({})


def delete_bulk(request, viewmodel):
    serializer = DeleteThreadsSerializer(
        data={
            'threads': request.data,
        },
        context={
            'request': request,
            'viewmodel': viewmodel,
        },
    )

    serializer.is_valid(raise_exception=True)

    for thread in serializer.validated_data['threads']:
        with transaction.atomic():
            delete_thread(request, thread)

    return Response([])


def hydrate_error_details(errors):
    for error in errors:
        error['thread']['id'] = int(error['thread']['id'])
    return errors
