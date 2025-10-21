from typing import TYPE_CHECKING, Optional
from urllib.parse import quote_plus

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import pgettext

from ...notifications.tasks import notify_on_new_private_thread
from ...permissions.privatethreads import (
    check_change_private_thread_owner_permission,
    check_remove_private_thread_member_permission,
)
from ...permissions.proxy import UserPermissionsProxy
from ...threads.models import Thread
from ...threads.views.generic import PrivateThreadView
from ...threadupdates.create import create_added_member_thread_update
from ...threadupdates.models import ThreadUpdate
from ...threads.nexturl import get_next_thread_url
from ...threads.postsfeed import PrivateThreadPostsFeed
from ..forms import MembersAddForm
from ..members import (
    change_private_thread_owner,
    private_thread_has_members,
    remove_private_thread_member,
)
from ..models import PrivateThreadMember
from ..validators import validate_new_private_thread_owner

if TYPE_CHECKING:
    from ...users.models import User


class PrivateThreadMembersAddView(PrivateThreadView):
    thread_get_members = True
    form_type = MembersAddForm
    template_name = "misago/private_thread_members_add/index.html"
    template_name_htmx = "misago/private_thread_members_add/htmx.html"

    def get(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        form = self.form_type(
            request=request,
            owner=self.owner,
            members=self.members,
        )

        return self.render_form_page(request, thread, form)

    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        form = self.form_type(
            request.POST,
            request=request,
            owner=self.owner,
            members=self.members,
        )

        if form.is_valid():
            return self.handle_form(request, thread, form)

        return self.render(request, thread, form)

    def handle_form(
        self, request: HttpRequest, thread: Thread, form: MembersAddForm
    ) -> HttpResponse:
        thread_updates = []

        new_members = form.cleaned_data["users"]
        if new_members:
            for member in new_members:
                PrivateThreadMember.objects.create(thread=thread, user=member)
                thread_update = create_added_member_thread_update(
                    thread, member, self.request.user, request
                )
                thread_updates.append(thread_update)

            notify_on_new_private_thread.delay(
                request.user.id, thread.id, [user.id for user in new_members]
            )

            messages.success(
                request,
                pgettext("private thread members add view", "New members added"),
            )

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread))

        response = PrivateThreadMembersHtmxResponse(
            request, thread, self.owner, self.members + new_members
        )

        if thread_update:
            response.set_thread_updates([thread_update])

        return response.render(
            {"swap_oob": True},
            {"hx-trigger": "misago:afterUpdateMembers", "hx-reswap": "none"},
        )

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)

        if not (
            self.get_moderator_status(request, thread)
            or self.get_owner_status(request, thread)
        ):
            raise PermissionDenied(
                pgettext(
                    "private thread add members view",
                    "You can't add members to this thread.",
                )
            )

        return thread

    def render_form_page(
        self, request: HttpRequest, thread: Thread, form: MembersAddForm
    ):
        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(
            request,
            template_name,
            {
                "thread": thread,
                "members": self.members,
                "form": form,
                "next_url": self.get_next_thread_url(request, thread),
            },
        )


class PrivateThreadMemberView(PrivateThreadView):
    thread_get_members = True
    template_name: str

    def get(
        self, request: HttpRequest, thread_id: int, slug: str, user_id: int
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        try:
            member = self.get_member(request, user_id)
        except Http404 as error:
            if request.is_htmx:
                raise

            messages.error(request, str(error))
            return redirect(self.get_next_thread_url(request, thread, strip_qs=True))

        self.check_permissions(request, thread, member)

        member_permissions = UserPermissionsProxy(member, request.cache_versions)
        check_remove_private_thread_member_permission(
            request.user_permissions, thread, member_permissions
        )

        return render(
            request,
            self.template_name,
            {
                "thread": thread,
                "member": member,
                "next_url": self.get_next_thread_url(request, thread, strip_qs=True),
            },
        )

    def post(
        self, request: HttpRequest, thread_id: int, slug: str, user_id: int
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        try:
            member = self.get_member(request, user_id)
        except Http404 as error:
            if request.is_htmx:
                raise

            messages.error(request, str(error))
            return redirect(self.get_next_thread_url(request, thread, strip_qs=True))

        self.check_permissions(request, thread, member)

        thread_update = self.update_members(request, thread, member)

        if not request.is_htmx:
            return redirect(self.get_next_thread_url(request, thread))

        response = PrivateThreadMembersHtmxResponse(
            request, thread, self.owner, self.members
        )
        if thread_update:
            response.set_thread_updates([thread_update])

        return response.render()

    def update_members(
        self, request: HttpRequest, thread: Thread, member: "User"
    ) -> ThreadUpdate | None:
        return None

    def get_member(self, request: HttpRequest, user_id: int) -> "User":
        for member in self.members:
            if member.id == user_id:
                return member

        raise Http404(pgettext("private thread member view", "Member doesn't exist"))

    def check_permissions(self, request: HttpRequest, thread: Thread, member: "User"):
        pass


class PrivateThreadOwnerChangeView(PrivateThreadMemberView):
    template_name = "misago/private_thread_owner_change/index.html"

    def update_members(
        self, request: HttpRequest, thread: Thread, member: "User"
    ) -> ThreadUpdate | None:
        if member == self.owner:
            return None

        thread_update = change_private_thread_owner(
            request.user, thread, member, request
        )
        self.owner = member

        messages.success(
            request,
            pgettext("add private thread owner change view", "Owner changed"),
        )

        return thread_update

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)

        if not (
            self.get_moderator_status(request, thread)
            or self.get_owner_status(request, thread)
        ):
            raise PermissionDenied(
                pgettext(
                    "private thread owner change view",
                    "You can't change this thread's owner.",
                )
            )

        return thread

    def check_permissions(self, request: HttpRequest, thread: Thread, member: "User"):
        check_change_private_thread_owner_permission(request.user_permissions, thread)

        try:
            member_permissions = UserPermissionsProxy(member, request.cache_versions)
            validate_new_private_thread_owner(
                member_permissions,
                request.user_permissions,
                request.cache_versions,
                request,
            )
        except ValidationError as error:
            raise PermissionDenied(error.messages[0])


class PrivateThreadMemberRemoveView(PrivateThreadMemberView):
    template_name = "misago/private_thread_member_remove/index.html"

    def update_members(
        self, request: HttpRequest, thread: Thread, member: "User"
    ) -> ThreadUpdate | None:
        if member == self.owner:
            return None

        thread_update = remove_private_thread_member(
            request.user, thread, member, request
        )

        self.members.remove(member)

        messages.success(
            request,
            pgettext("private thread member remove view", "Member removed"),
        )

        return thread_update

    def check_permissions(self, request: HttpRequest, thread: Thread, member: "User"):
        member_permissions = UserPermissionsProxy(member, request.cache_versions)
        check_remove_private_thread_member_permission(
            request.user_permissions, thread, member_permissions
        )


class PrivateThreadLeaveView(PrivateThreadView):
    template_name = "misago/private_thread_leave/index.html"

    def get(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        return render(
            request,
            self.template_name,
            {
                "thread": thread,
                "next_url": self.get_next_thread_url(request, thread, strip_qs=True),
            },
        )

    def post(self, request: HttpRequest, thread_id: int, slug: str) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        remove_private_thread_member(request.user, thread, request.user, request)

        messages.success(
            request,
            pgettext("private thread leave view", "Left the thread"),
        )

        if not private_thread_has_members(thread):
            thread.delete()

        return redirect(reverse("misago:private-thread-list"))


class PrivateThreadMembersHtmxResponse:
    template_name = "misago/private_thread_members/htmx.html"

    request: HttpRequest
    thread: Thread
    owner: Optional["User"]
    members: list["User"]
    thread_updates: Optional[list[ThreadUpdate]]

    def __init__(
        self,
        request: HttpRequest,
        thread: Thread,
        owner: Optional["User"],
        members: list["User"],
    ):
        self.request = request
        self.thread = thread
        self.owner = owner
        self.members = members
        self.thread_updates = None

    def set_thread_updates(self, thread_updates: list[ThreadUpdate]):
        self.thread_updates = thread_updates

    def get_context(self):
        context = get_private_thread_members_context_data(
            self.request, self.thread, self.owner, self.members
        )
        if self.thread_updates:
            context["feed"] = self.get_feed_context()
        return context

    def get_feed_context(self):
        posts_feed = PrivateThreadPostsFeed(
            self.request, self.thread, [], self.thread_updates
        )

        posts_feed.set_animated_thread_updates(
            [thread_update.id for thread_update in self.thread_updates]
        )

        return posts_feed.get_context_data()

    def render(
        self, context: dict | None = None, headers: dict | None = None
    ) -> HttpResponse:
        final_context = self.get_context()
        final_context["open"] = True

        if context:
            final_context.update(context)

        response = render(self.request, self.template_name, final_context)

        if headers:
            for header, value in headers.items():
                response[header] = value

        return response


def get_private_thread_members_context_data(
    request: HttpRequest,
    thread: Thread,
    owner: Optional["User"],
    members: list["User"],
) -> dict:
    moderation = bool(request.user_permissions.is_private_threads_moderator)
    manage = moderation or request.user.id == owner.id if owner else None

    next_url = get_next_thread_url(request, thread, "misago:private-thread")
    next_url_quoted = quote_plus(next_url)

    add_members_url = (
        reverse(
            "misago:private-thread-members-add",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"?next={next_url_quoted}"
    )

    return {
        "manage": manage,
        "moderation": moderation,
        "thread": thread,
        "owner": owner,
        "members": members,
        "template_name": "misago/private_thread_members/index.html",
        "add_members_url": add_members_url,
        "next_url_quoted": next_url_quoted,
    }
