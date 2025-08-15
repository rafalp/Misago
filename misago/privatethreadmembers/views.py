from typing import TYPE_CHECKING, Optional

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import pgettext

from ..notifications.tasks import notify_on_new_private_thread
from ..threads.models import Thread
from ..threads.views.generic import PrivateThreadView
from ..threadupdates.create import create_added_member_thread_update
from .forms import PrivateThreadAddMembersForm
from .models import PrivateThreadMember

if TYPE_CHECKING:
    from ..users.models import User


class PrivateThreadAddMembersView(PrivateThreadView):
    thread_get_members = True
    form_type = PrivateThreadAddMembersForm
    template_name = "misago/add_private_thread_members/index.html"
    template_name_htmx = "misago/add_private_thread_members/form.html"

    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)

        form = self.form_type(
            request=request,
            owner=self.owner,
            members=self.members,
        )

        return self.render_form_page(request, thread, form)

    def post(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, id)

        form = self.form_type(
            request.POST,
            request=request,
            owner=self.owner,
            members=self.members,
        )

        if form.is_valid():
            new_members = form.cleaned_data["users"]
            for member in new_members:
                PrivateThreadMember.objects.create(thread=thread, user=member)
                create_added_member_thread_update(thread, member, self.request.user, request)

            notify_on_new_private_thread(request.user.id, thread.id, [user.id for user in new_members])

            messages.success(request, pgettext("add private thread members view", "New members added"))

            return redirect(self.get_thread_url(thread))

        return self.render(request, thread, form)

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        if request.user.is_anonymous:
            raise PermissionDenied(
                pgettext(
                    "add private thread members view",
                    "You must be signed in to add members to a private thread.",
                )
            )

        thread = super().get_thread(request, thread_id)

        if not (
            self.get_moderator_status(request, thread)
            or self.get_owner_status(request, thread)
        ):
            raise PermissionDenied(
                pgettext(
                    "add private thread members view",
                    "You can't add members to this thread.",
                )
            )

        return thread

    def render_form_page(
        self, request: HttpRequest, thread: Thread, form: PrivateThreadAddMembersForm
    ):
        return render(
            request,
            self.template_name,
            {
                "thread": thread,
                "members": self.members,
                "form": form,
                "template_name_htmx": self.template_name_htmx,
            },
        )


def get_private_thread_members_context_data(
    request: HttpRequest,
    thread: Thread,
    owner: Optional["User"],
    members: list["User"],
) -> dict:
    moderation = bool(request.user_permissions.is_private_threads_moderator)
    manage = moderation or request.user.id == owner.id if owner else None

    return {
        "manage": manage,
        "moderation": moderation,
        "thread": thread,
        "owner": owner,
        "members": members,
        "add_members_url": reverse(
            "misago:private-thread-add-members",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
    }
