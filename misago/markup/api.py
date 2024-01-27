from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..parser.context import create_parser_context
from ..parser.factory import create_parser
from ..parser.html import complete_markup_html, render_ast_to_html
from ..parser.metadata import create_ast_metadata
from . import common_flavour, finalize_markup
from .serializers import MarkupSerializer


@api_view(["POST"])
def parse_markup(request):
    serializer = MarkupSerializer(
        data=request.data, context={"settings": request.settings}
    )
    if not serializer.is_valid():
        errors_list = list(serializer.errors.values())[0]
        return Response({"detail": errors_list[0]}, status=status.HTTP_400_BAD_REQUEST)

    context = create_parser_context(request)
    parse = create_parser(context)
    ast = parse(serializer.data["post"])
    import json

    print(json.dumps(ast, indent=2))
    metadata = create_ast_metadata(context, ast)
    return Response(
        {"parsed": complete_markup_html(render_ast_to_html(context, ast, metadata))}
    )

    parsing_result = common_flavour(
        request, request.user, serializer.data["post"], force_shva=True
    )
    finalized = finalize_markup(parsing_result["parsed_text"])

    return Response({"parsed": finalized})
