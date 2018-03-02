from rest_framework.response import Response

from django.db import IntegrityError
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.users.namechanges import get_available_namechanges_data
from misago.users.serializers import ChangeUsernameSerializer


def username_endpoint(request):
    if request.method == 'POST':
        return change_username(request)
    else:
        form_options = get_available_namechanges_data(request.user)
        form_options.update({
            'length_min': settings.username_length_min,
            'length_max': settings.username_length_max,
        })
        
        return Response(form_options)


def change_username(request):
    available_namechanges = get_available_namechanges_data(request.user)
    if not available_namechanges['changes_left']:
        return Response(
            {
                'username': [_("You can't change your username at this time.")],
                'next_change_on': available_namechanges['next_change_on'],
            },
            status=400,
        )

    serializer = ChangeUsernameSerializer(
        data=request.data,
        context={'user': request.user},
    )

    serializer.is_valid(raise_exception=True)

    try:
        serializer.change_username(changed_by=request.user)

        response_data = get_available_namechanges_data(request.user)
        response_data.update({
            'username': request.user.username,
            'slug': request.user.slug,
        })

        return Response(response_data)
    except IntegrityError:
        return Response(
            {
                'username': [_("Please try again.")],
            },
            status=400,
        )


def moderate_username_endpoint(request, profile):
    if request.method == 'POST':
        serializer = ChangeUsernameSerializer(data=request.data, context={'user': profile})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.change_username(changed_by=request.user)
            return Response({
                'username': profile.username,
                'slug': profile.slug,
            })
        except IntegrityError:
            return Response(
                {
                    'username': [_("Please try again.")],
                },
                status=400,
            )
    else:
        # return form data
        return Response({
            'length_min': settings.username_length_min,
            'length_max': settings.username_length_max,
        })
