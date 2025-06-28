from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ...permissions.checkutils import check_permissions
from ...permissions.threads import check_vote_in_thread_poll_permission
from ...polls.choices import PollChoices
from ...polls.models import Poll
from ...polls.votes import delete_user_poll_votes, get_user_poll_votes, save_user_poll_vote
from ..models import Thread
from .generic import ThreadView


class PollView():
    poll_results_template_name_htmx = "misago/poll/results_partial.html"
    poll_vote_template_name_htmx = "misago/poll/vote_partial.html"
    poll_results_url_name = "misago:thread-poll-results"
    poll_vote_url_name = "misago:thread-poll-vote"

    def get_poll_context_data(self, request: HttpRequest, thread: Thread, poll: Poll) -> dict:
        user_poll_votes = set()
        if request.user.is_authenticated:
            user_poll_votes = get_user_poll_votes(request.user, poll)

        with check_permissions() as allow_vote:
            check_vote_in_thread_poll_permission(request.user_permissions, thread.category, thread, poll)

        template_name = self.poll_results_template_name_htmx
        if allow_vote and request.user.is_authenticated and not user_poll_votes:
            template_name = self.poll_vote_template_name_htmx

        poll_results_url = reverse(
            self.poll_results_url_name, kwargs={"id": thread.id, "slug": thread.slug}
        )

        poll_vote_url = None
        if allow_vote and request.user.is_authenticated:
            poll_vote_url = reverse(
                self.poll_vote_url_name, kwargs={"id": thread.id, "slug": thread.slug}
            )

        return {
            "poll": poll,
            "template_name": template_name,
            "user_poll_votes": user_poll_votes,
            "question": poll.question,
            "allow_poll_vote": allow_vote,
            "poll_results_url": poll_results_url,
            "poll_vote_url": poll_vote_url,
        }


class ThreadPollView(PollView, ThreadView, View):
    def get_poll(self, request: HttpRequest, thread: Thread) -> Poll:
        poll = super().get_poll(request, thread)
        if not poll:
            raise Http404()
        return poll


class ThreadPollVoteView(ThreadPollView):
    template_name = "misago/polls/vote.html"

    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        poll = self.get_poll(request, thread)
        
        if request.is_htmx:
            template_name = self.poll_vote_template_name_htmx
        else:
            template_name = self.template_name

        return render(
            request,
            template_name,
            self.get_poll_context_data(request, thread, poll)
        )

    def post(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        poll = self.get_poll(request, thread)

        poll_choices = PollChoices(poll.choices)

        user_choices = request.POST.getlist("poll_choice")
        valid_choices = set(poll_choices.ids()).intersection(user_choices)

        if not valid_choices:
            raise PermissionError("SELECT ANY CHOICE YOU PLEB")
        
        if len(valid_choices) > poll.max_choices:
            raise PermissionError("YOU SELECTED TOO MANY CHOICES YOU PLEB")

        if user_poll_votes := get_user_poll_votes(request.user, poll):
            delete_user_poll_votes(request.user, poll, user_poll_votes)

        save_user_poll_vote(request.user, poll, valid_choices)

        if request.is_htmx:
            template_name = self.poll_results_template_name_htmx
        else:
            template_name = self.template_name

        return render(
            request,
            template_name,
            self.get_poll_context_data(request, thread, poll)
        )


class ThreadPollResultsView(ThreadPollView):
    template_name = "misago/polls/results.html"

    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)
        poll = self.get_poll(request, thread)
        raise Http404()
