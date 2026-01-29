from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import pgettext

from ..permissions.checkutils import check_permissions
from ..permissions.polls import (
    check_close_thread_poll_permission,
    check_delete_thread_poll_permission,
    check_edit_thread_poll_permission,
    check_open_thread_poll_permission,
    check_start_thread_poll_permission,
    check_vote_in_thread_poll_permission,
)
from ..threads.postfeed import ThreadPostFeed
from ..threads.models import Thread
from ..threads.nexturl import get_next_thread_url
from ..threads.views.generic import ThreadView
from ..threadupdates.models import ThreadUpdate
from ..polls.models import Poll
from .close import close_thread_poll, open_thread_poll
from .delete import delete_thread_poll
from .enums import PollTemplate, PublicPollsAvailability
from .forms import EditPollForm, StartPollForm
from .save import edit_thread_poll, save_thread_poll
from .validators import validate_poll_vote
from .votes import (
    delete_user_poll_votes,
    get_poll_results_data,
    get_user_poll_votes,
    save_user_poll_vote,
)


class ThreadPollView(ThreadView):
    def get_poll(self, request: HttpRequest, thread: Thread) -> Poll | None:
        poll = Poll.objects.filter(thread=thread).first()
        if not poll:
            raise Http404()

        poll.category = thread.category
        poll.thread = thread

        return poll


class StartThreadPollView(ThreadView):
    template_name = "misago/poll/start.html"

    def get(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        check_start_thread_poll_permission(
            request.user_permissions, thread.category, thread
        )

        form = StartPollForm(request=request)
        return self.render(request, thread, form)

    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        check_start_thread_poll_permission(
            request.user_permissions, thread.category, thread
        )

        form = StartPollForm(request.POST, request=request)
        if form.is_valid():
            poll = form.create_poll_instance(thread.category, thread, request.user)
            save_thread_poll(thread, poll, request.user, request)

            messages.success(request, pgettext("start poll", "Poll started"))
            return redirect(
                reverse(
                    "misago:thread",
                    kwargs={"thread_id": thread.id, "slug": thread.slug},
                )
            )

        return self.render(request, thread, form)

    def render(
        self, request: HttpRequest, thread: Thread, form: EditPollForm
    ) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {
                "category": thread.category,
                "thread": thread,
                "form": form,
            },
        )


class EditThreadPollView(ThreadPollView):
    template_name = "misago/poll/edit.html"
    template_name_htmx = "misago/poll/edit_partial.html"

    def get(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)

        check_edit_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

        form = EditPollForm(instance=poll, request=request)
        return self.render(request, thread, poll, form)

    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)

        check_edit_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

        form = EditPollForm(request.POST, instance=poll, request=request)
        if form.is_valid():
            return self.handle_form(request, thread, poll, form)

        return self.render(request, thread, poll, form)

    def handle_form(
        self, request: HttpRequest, thread: Thread, poll: Poll, form: EditPollForm
    ) -> HttpResponse:
        poll = form.update_poll_instance()
        edit_thread_poll(thread, poll, request.user, request)

        messages.success(request, pgettext("edit poll", "Poll edited"))

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread, poll))

        user_poll_votes = get_user_poll_votes(request.user, poll)
        context = get_poll_context_data(request, thread, poll, user_poll_votes)

        with check_permissions() as allow_vote:
            check_vote_in_thread_poll_permission(
                request.user_permissions, thread.category, thread, poll
            )

        if allow_vote and not user_poll_votes:
            template_name = PollTemplate.VOTE_HTMX
        else:
            template_name = PollTemplate.RESULTS_HTMX

        return render(request, template_name, context)

    def render(
        self, request: HttpRequest, thread: Thread, poll: Poll, form: EditPollForm
    ) -> HttpResponse:
        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(
            request,
            template_name,
            {
                "category": thread.category,
                "thread": thread,
                "form": form,
                "next_url": self.get_next_thread_url(request, thread, poll),
            },
        )

    def get_next_thread_url(
        self, request: HttpRequest, thread: Thread, poll: Poll
    ) -> str:
        next_url = super().get_next_thread_url(request, thread, strip_qs=True)

        if not request.is_htmx:
            return next_url

        with check_permissions() as allow_vote:
            check_vote_in_thread_poll_permission(
                request.user_permissions, thread.category, thread, poll
            )

        user_poll_votes = get_user_poll_votes(request.user, poll)
        if allow_vote and not user_poll_votes:
            return f"{next_url}?poll=vote"

        return f"{next_url}?poll=results"


class ThreadPollVoteView(ThreadPollView):
    def get(self, request: HttpRequest, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)
        user_poll_votes = get_user_poll_votes(request.user, poll)

        check_vote_in_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

        context = get_poll_context_data(request, thread, poll, user_poll_votes)
        return render(request, PollTemplate.VOTE_HTMX, context)

    def post(self, request: HttpRequest, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)
        user_poll_votes = get_user_poll_votes(request.user, poll)

        check_vote_in_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

        if user_poll_votes and not poll.can_change_vote:
            raise PermissionDenied(
                pgettext("poll vote", "This poll doesn't allow vote changes.")
            )

        user_choices = request.POST.getlist("poll_choice")

        try:
            valid_choices = validate_poll_vote(
                user_choices, poll.choices, poll.max_choices
            )
        except ValidationError as error:
            return self.get_error_response(request, thread, poll, user_choices, error)

        if valid_choices != user_poll_votes:
            if user_poll_votes:
                delete_user_poll_votes(request.user, poll, user_poll_votes)

            save_user_poll_vote(request.user, poll, valid_choices)
            messages.success(request, pgettext("poll vote", "Vote saved"))

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread))

        context = get_poll_context_data(request, thread, poll, valid_choices)
        return render(request, PollTemplate.RESULTS_HTMX, context)

    def get_error_response(
        self,
        request: HttpRequest,
        thread: Thread,
        poll: Poll,
        user_poll_votes: set[str],
        error: ValidationError,
    ) -> HttpResponse:
        error_message = error.messages[0]

        if not request.is_htmx:
            messages.error(request, error_message)
            return redirect(self.get_next_thread_url(request, thread))

        context = get_poll_context_data(request, thread, poll, user_poll_votes)
        context["poll_error_message"] = error_message
        return render(request, PollTemplate.VOTE_HTMX, context)


class ThreadPollResultsView(ThreadPollView):
    def get(
        self, request: HttpRequest, thread_id: int, show_voters: bool = False
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)
        user_poll_votes = get_user_poll_votes(request.user, poll)

        context = get_poll_context_data(
            request, thread, poll, user_poll_votes, show_voters
        )

        return render(request, PollTemplate.RESULTS_HTMX, context)


thread_poll_results = ThreadPollResultsView.as_view()
thread_poll_vote = ThreadPollVoteView.as_view()


def dispatch_thread_poll_view(
    request: HttpRequest, thread_id: int
) -> HttpResponse | None:
    view = request.GET.get("poll")
    if not view:
        return None

    if view in ("results", "voters"):
        return thread_poll_results(request, thread_id, view == "voters")
    if view == "vote":
        return thread_poll_vote(request, thread_id)

    return None


class UpdateThreadPollView(ThreadPollView):
    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)

        self.check_permission(request, thread, poll)

        thread_update = self.update(request, thread, poll)

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread))

        user_poll_votes = get_user_poll_votes(request.user, poll)
        context = get_poll_context_data(request, thread, poll, user_poll_votes)

        if thread_update:
            post_feed = ThreadPostFeed(request, thread, [], [thread_update])
            post_feed.set_animated_thread_updates([thread_update.id])
            context["feed"] = post_feed.get_context_data()

        if context["allow_vote"] and not user_poll_votes:
            template_name = PollTemplate.VOTE_HTMX
        else:
            template_name = PollTemplate.RESULTS_HTMX

        return render(request, template_name, context)

    def check_permission(self, request: HttpRequest, thread: Thread, poll: Poll):
        raise NotImplementedError()

    def update(
        self, request: HttpRequest, thread: Thread, poll: Poll
    ) -> ThreadUpdate | None:
        raise NotADirectoryError()


class CloseThreadPollView(UpdateThreadPollView):
    def check_permission(self, request: HttpRequest, thread: Thread, poll: Poll):
        check_close_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    def update(
        self, request: HttpRequest, thread: Thread, poll: Poll
    ) -> ThreadUpdate | None:
        thread_update = close_thread_poll(thread, poll, request.user, request)
        if thread_update:
            messages.success(request, pgettext("poll vote", "Poll closed"))

        return thread_update


class OpenThreadPollView(UpdateThreadPollView):
    def check_permission(self, request: HttpRequest, thread: Thread, poll: Poll):
        check_open_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    def update(
        self, request: HttpRequest, thread: Thread, poll: Poll
    ) -> ThreadUpdate | None:
        thread_update = open_thread_poll(thread, poll, request.user, request)
        if thread_update:
            messages.success(request, pgettext("poll vote", "Poll opened"))

        return thread_update


class DeleteThreadPollView(ThreadPollView):
    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        poll = self.get_poll(request, thread)

        check_delete_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

        delete_thread_poll(thread, poll, request.user, request)

        messages.success(request, pgettext("poll vote", "Poll deleted"))

        return redirect(self.get_next_thread_url(request, thread))


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
    enable_public_polls = (
        request.settings.enable_public_polls != PublicPollsAvailability.DISABLED
    )

    show_voters = poll.is_public and fetch_voters and enable_public_polls
    poll_results = get_poll_results_data(poll, show_voters)

    with check_permissions() as allow_edit:
        check_edit_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    with check_permissions() as allow_close:
        check_close_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    with check_permissions() as allow_open:
        check_open_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    with check_permissions() as allow_delete:
        check_delete_thread_poll_permission(
            request.user_permissions, thread.category, thread, poll
        )

    thread_url = get_next_thread_url(request, thread, "misago:thread")

    return {
        "poll": poll,
        "is_public": poll.is_public and enable_public_polls,
        "user_votes": user_poll_votes,
        "question": poll.question,
        "results": poll_results,
        "show_voters": show_voters,
        "allow_edit": allow_edit,
        "allow_close": allow_close and not poll.is_closed,
        "allow_open": allow_open and poll.is_closed,
        "allow_delete": allow_delete,
        "allow_vote": allow_vote,
        "edit_url": reverse(
            "misago:thread-poll-edit",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        "close_url": reverse(
            "misago:thread-poll-close",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        "open_url": reverse(
            "misago:thread-poll-open",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        "delete_url": reverse(
            "misago:thread-poll-delete",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        "next_url": thread_url,
        "results_url": f"{thread_url}?poll=results",
        "voters_url": f"{thread_url}?poll=voters",
        "vote_url": f"{thread_url}?poll=vote",
    }
