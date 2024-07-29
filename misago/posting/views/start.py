from django.http import HttpRequest, HttpResponse
from django.views import View


class StartView(View):
    pass


class ThreadStartView(StartView):
    pass


class PrivateThreadStartView(StartView):
    pass


def select_category(request: HttpRequest) -> HttpResponse:
    pass
