from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import common_flavour, finalise_markup
from .serializers import MarkupSerializer


@api_view(["POST"])
def parse_markup(request):
    serializer = MarkupSerializer(
        data=request.data, context={"settings": request.settings}
    )
    if not serializer.is_valid():
        errors_list = list(serializer.errors.values())[0]
        return Response({"detail": errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)

    parsing_result = common_flavour(
        request, request.user, serializer.data["post"], force_shva=True
    )
    finalised = finalise_markup(parsing_result["parsed_text"])

    return Response({"parsed": finalised})
