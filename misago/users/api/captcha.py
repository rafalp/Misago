from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def question(request):
    if not request.settings.qa_question:
        raise Http404()

    return Response(
        {
            "question": request.settings.qa_question,
            "help_text": request.settings.qa_help_text,
        }
    )
