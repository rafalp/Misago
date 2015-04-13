from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from misago.conf import settings


@api_view(['GET', 'POST'])
def question(request, question_id):
    try:
        question_id = int(question_id)
    except TypeError:
        raise Http404()

    if settings.qa_question and question_id == 1:
        return Response({
            'id': question_id,
            'question': settings.qa_question,
            'help_text': settings.qa_help_text,
        })
    else:
        raise Http404()
