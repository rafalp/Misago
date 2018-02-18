from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

from misago.threads.validators import validate_post_length

from . import common_flavour, finalise_markup


@api_view(['POST'])
def parse_markup(request):
    serializer = MarkupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    parsing_result = common_flavour(
        request,
        request.user,
        serializer.data['markup'],
        force_shva=True,
    )
    finalised = finalise_markup(parsing_result['parsed_text'])

    return Response({'parsed': finalised})


class MarkupSerializer(serializers.Serializer):
    markup = serializers.CharField(allow_blank=True)

    def validate_markup(self, data):
        validate_post_length(data)
        return data
