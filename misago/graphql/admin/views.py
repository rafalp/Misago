import json

from ariadne import QueryType, graphql_sync, make_executable_schema
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


type_defs = """
    type Query {
        hello: String!
    }
"""

query = QueryType()


@query.field("hello")
def resolve_hello(*_):
    return "Hello Misago Admin!"


schema = make_executable_schema(type_defs, query)


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
