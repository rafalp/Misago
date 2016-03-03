from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from misago.users.rest_permissions import IsAuthenticatedOrReadOnly

from misago.threads.api.threadendpoints.list import threads_list_endpoint

class ThreadViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    parser_classes=(JSONParser, )

    def list(self, request):
        return threads_list_endpoint(request)