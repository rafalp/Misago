from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404


@api_view()
def question(request):
    if request.settings.qa_question:
        return Response({
            'question': request.settings.qa_question,
            'help_text': request.settings.qa_help_text,
        })
    else:
        raise Http404()
