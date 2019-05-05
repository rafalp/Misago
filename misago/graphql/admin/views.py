import json

from ariadne import (
    QueryType,
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
)
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .schema import schema


@csrf_exempt
def graphql_view(request):
    if request.method == "GET":
        return render(request, "misago/admin/graphql_playground.html")

    if request.method != "POST":
        return HttpResponseBadRequest()

    if request.content_type != "application/json":
        return HttpResponseBadRequest()

    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest()

    success, result = graphql_sync(
        schema, data, context_value=request, debug=settings.DEBUG
    )

    status_code = 200 if success else 400
    return JsonResponse(result, status=status_code)
