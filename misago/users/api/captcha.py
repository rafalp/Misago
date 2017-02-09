from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from misago.conf import settings


@api_view()
def question(request):
    if settings.qa_question:
        return Response({
            'question': settings.qa_question,
            'help_text': settings.qa_help_text,
        })
    else:
        raise Http404()
