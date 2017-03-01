from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.core.exceptions import ValidationError
from django.utils import six

from misago.threads.validators import validate_post_length

from . import common_flavour, finalise_markup


@api_view(['POST'])
def parse_markup(request):
    post = six.text_type(request.data.get('post', '')).strip()

    try:
        validate_post_length(post)
    except ValidationError as e:
        return Response({'detail': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    parsed = common_flavour(request, request.user, post, force_shva=True)['parsed_text']
    finalised = finalise_markup(parsed)

    return Response({'parsed': finalised})
