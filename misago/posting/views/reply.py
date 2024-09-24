from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import pgettext

from ...auth.decorators import login_required
from ...threads.models import Thread
from ..state.reply import ReplyPrivateThreadState, ReplyThreadState


def reply_thread_login_required():
    return login_required(
        pgettext(
            "reply thread page",
            "Sign in to reply to threads",
        )
    )


class ReplyThreadView(View):
    template_name: str = "misago/posting/reply_thread.html"
    state_class = ReplyThreadState

    @method_decorator(reply_thread_login_required())
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        thread = self.get_thread(request, kwargs)
        formset = self.get_formset(request, thread)

        return render(
            request,
            self.template_name,
            self.get_context_data(request, thread, formset),
        )

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        thread = self.get_thread(request, kwargs)
        formset = self.get_formset(request, thread)

    def get_thread(self, request: HttpRequest, kwargs: dict) -> Thread:
        try:
            thread = Thread.objects.get(id=kwargs["id"])
        except Thread.DoesNotExist:
            raise Http404()

        return thread


class ReplyPrivateThreadView(ReplyThreadView):
    pass
