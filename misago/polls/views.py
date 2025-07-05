from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import pgettext
from django.views import View

from ..permissions.checkutils import check_permissions
from ..permissions.threads import (
    check_close_thread_poll_permission,
    check_edit_thread_poll_permission,
    check_see_thread_permission,
    check_vote_in_thread_poll_permission,
)
from ..threads.models import Thread
from ..polls.models import Poll
from .choices import PollChoices
from .delete import delete_poll
from .enums import PollTemplate
from .forms import StartPollForm
from .validators import validate_poll_vote
from .votes import (
    delete_user_poll_votes,
    get_poll_results_data,
    get_user_poll_votes,
    save_user_poll_vote,
)


def dispatch_poll_view(request: HttpRequest, thread_id: int) -> HttpResponse | None:
    view = request.GET.get("poll")
    if not view:
        return None

    if request.method == "POST":
        if view == "edit":
            raise NotImplementedError()
        if view == "close":
            raise NotImplementedError()
        if view == "open":
            raise NotImplementedError()
        if view == "delete":
            return poll_delete(request, thread_id)
        if view == "vote":
            return poll_vote(request, thread_id)
    elif request.is_htmx:
        if view == "start":
            return poll_vote(request, thread_id)
        if view in ("results", "voters"):
            return poll_results(request, thread_id, view == "voters")
        if view == "vote":
            return poll_vote(request, thread_id)

    return None


class PollView(View):
    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        queryset = Thread.objects.select_related("category")
        thread = get_object_or_404(queryset, id=thread_id)
        check_see_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_poll(self, request: HttpRequest, thread: Thread) -> Poll | None:
        poll = Poll.objects.filter(thread=thread).first()
        if not poll:
            raise Http404()

        poll.category = thread.category
        poll.thread = thread

        return poll


class PollStartView(PollView):
    template_name = "misago/poll/start.html"

    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        if thread.has_poll:
            pass

        form = StartPollForm(request=request)
        return self.render(request, thread, form)

    def post(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        if thread.has_poll:
            pass

        form = StartPollForm(request.POST, request=request)
        if form.is_valid():
            form.save(thread.category, thread, request.user)
            thread.has_poll = True
            thread.save(update_fields=["has_poll"])

            messages.success(request, pgettext("start poll", "Poll started"))
            return redirect(reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}))

        return self.render(request, thread, form)

    def render(self, request: HttpRequest, thread: Thread, form: StartPollForm) -> HttpResponse:
        return render(request, self.template_name, {
            "category": thread.category,
            "thread": thread,
            "form": form,
        })


class PollResultsView(PollView):
    def get(self, request: HttpRequest, thread_id: int, show_voters: bool = False) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)
        user_poll_votes = get_user_poll_votes(request.user, poll)

        context = get_poll_context_data(
            request, thread, poll, user_poll_votes, show_voters
        )
        return render(request, PollTemplate.RESULTS, context)


class PollVoteView(PollView):
    def get(self, request: HttpRequest, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)
        user_poll_votes = get_user_poll_votes(request.user, poll)

        check_vote_in_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

        context = get_poll_context_data(request, thread, poll, user_poll_votes)
        return render(request, PollTemplate.VOTE, context)

    def post(self, request: HttpRequest, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)
        user_poll_votes = get_user_poll_votes(request.user, poll)

        check_vote_in_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

        if user_poll_votes and not poll.can_change_vote:
            raise PermissionDenied(
                pgettext("poll vote", "This poll doesn’t allow vote changes.")
            )

        poll_choices = PollChoices(poll.choices)
        user_choices = request.POST.getlist("poll_choice")

        valid_choices = validate_poll_vote(user_choices, poll_choices, poll.max_choices)

        if valid_choices != user_poll_votes:
            if user_poll_votes:
                delete_user_poll_votes(request.user, poll, user_poll_votes)

            save_user_poll_vote(request.user, poll, valid_choices)
            messages.success(request, pgettext("poll vote", "Vote saved"))

        if not request.is_htmx:
            return redirect(request.path)

        context = get_poll_context_data(request, thread, poll, valid_choices)
        context["show_poll_snackbars"] = True

        return render(request, PollTemplate.RESULTS, context)


class PollDeleteView(PollView):
    def post(self, request: HttpRequest, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)

        delete_poll(poll, request)
        thread.has_poll = False
        thread.save(update_fields=["has_poll"])

        messages.success(request, pgettext("poll vote", "Poll has been deleted"))

        return redirect(request.path)


poll_start = PollStartView.as_view()
poll_results = PollResultsView.as_view()
poll_vote = PollVoteView.as_view()
poll_delete = PollDeleteView.as_view()


def get_poll_context_data(
    request: HttpRequest,
    thread: Thread,
    poll: Poll,
    user_poll_votes: set[str],
    fetch_voters: bool = False,
) -> dict:
    with check_permissions() as allow_vote:
        check_vote_in_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    allow_vote = allow_vote and (not user_poll_votes or poll.can_change_vote)

    show_voters = poll.is_public and fetch_voters
    poll_results = get_poll_results_data(poll, show_voters)

    with check_permissions() as allow_edit:
        check_edit_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    with check_permissions() as allow_close:
        check_close_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    return {
        "poll": poll,
        "user_votes": user_poll_votes,
        "question": poll.question,
        "results": poll_results,
        "show_voters": show_voters,
        "moderator": request.user_permissions.is_category_moderator(poll.category_id),
        "allow_edit": allow_edit,
        "allow_close": allow_close and not poll.is_closed,
        "allow_vote": allow_vote,
        "edit_url": f"{request.path}?poll=edit",
        "close_url": f"{request.path}?poll=close",
        "open_url": f"{request.path}?poll=open",
        "delete_url": f"{request.path}?poll=delete",
        "voters_url": f"{request.path}?poll=voters",
        "vote_url": f"{request.path}?poll=vote",
    }
