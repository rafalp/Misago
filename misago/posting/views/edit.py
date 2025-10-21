from copy import copy
from typing import Iterable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.utils.translation import pgettext

from ...htmx.response import htmx_redirect
from ...permissions.privatethreads import (
    check_edit_private_thread_permission,
    check_edit_private_thread_post_permission,
)
from ...permissions.threads import (
    check_edit_thread_permission,
    check_edit_thread_post_permission,
)
from ...privatethreads.redirect import redirect_to_private_thread_post
from ...privatethreads.views.generic import PrivateThreadView
from ...threads.models import Post, Thread
from ...threads.prefetch import prefetch_posts_feed_related_objects
from ...threads.redirect import redirect_to_thread_post
from ...threads.views.generic import ThreadView
from ..hooks import (
    get_private_thread_edit_context_data_hook,
    get_private_thread_post_edit_context_data_hook,
    get_thread_edit_context_data_hook,
    get_thread_post_edit_context_data_hook,
)
from ..formsets import (
    Formset,
    PrivateThreadEditFormset,
    PrivateThreadPostEditFormset,
    ThreadEditFormset,
    ThreadPostEditFormset,
    get_private_thread_edit_formset,
    get_private_thread_post_edit_formset,
    get_thread_edit_formset,
    get_thread_post_edit_formset,
)
from ..state import (
    PostEditState,
    PrivateThreadPostEditState,
    ThreadPostEditState,
    get_private_thread_post_edit_state,
    get_thread_post_edit_state,
)
from ..validators import validate_posted_contents


class EditView(View):
    template_name: str
    template_name_htmx: str
    template_name_inline: str = "misago/inline_edit/index.html"
    template_name_inline_form: str = "misago/inline_edit/form.html"
    post_select_related: Iterable[str] = ("poster",)
    allow_edit_thread: bool = False

    def get(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int | None = None,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id or thread.first_post_id)
        formset = self.get_formset(request, post)
        return self.render(request, post, formset)

    def post(
        self,
        request: HttpRequest,
        thread_id: int,
        slug: str,
        post_id: int | None = None,
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        post = self.get_thread_post(request, thread, post_id or thread.first_post_id)
        state = self.get_state(request, post)

        # Short-circuit post handler if "cancel" button was pressed
        if self.is_inline(request) and request.POST.get("cancel"):
            return self.post_inline_edit(request, state, animate=False)

        formset = self.get_formset(request, post)

        # Detach thread and post from state for rendering
        # Prevents partially updated thread and post from appearing in UI
        # on validation errors
        post = copy(post)
        post.thread = copy(thread)

        formset.update_state(state)

        if formset.is_request_preview(request):
            formset.clear_errors_in_preview()
            return self.render(request, post, formset, state)

        if formset.is_request_upload(request):
            formset.clear_errors_in_upload()
            return self.render(request, post, formset)

        if not self.is_valid(formset, state):
            return self.render(request, post, formset)

        state.save()

        if post_id:
            success_message = pgettext("thread post edited", "Post edited")
        else:
            success_message = pgettext("thread edited", "Thread edited")

        messages.success(request, success_message)

        if post_id and self.is_inline(request):
            return self.post_inline_edit(request, state)

        if post_id:
            response = self.get_redirect_to_post(request, state.thread, state.post)
        else:
            response = redirect(self.get_thread_url(thread))

        if request.is_htmx:
            return htmx_redirect(response["location"])

        return response

    def post_inline_edit(
        self, request: HttpRequest, state: PostEditState, animate: bool = True
    ) -> HttpResponse:
        feed = self.get_posts_feed(request, state.thread, [state.post])

        if self.allow_edit_thread:
            feed.set_allow_edit_thread(True)

        if animate:
            feed.set_animated_posts([state.post.id])

        if state.post.id != state.thread.first_post_id:
            counter_start = (
                self.get_thread_posts_queryset(request, state.thread)
                .filter(id__lt=state.post.id)
                .count()
            )
            feed.set_counter_start(counter_start)

        post_context = feed.get_feed_data()[0]
        post_context["thread"] = state.thread

        return render(request, self.template_name_inline, context=post_context)

    def get_state(self, request: HttpRequest, post: Post) -> PostEditState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, post: Post) -> Formset:
        raise NotImplementedError()

    def is_valid(self, formset: Formset, state: PostEditState) -> bool:
        return formset.is_valid() and validate_posted_contents(formset, state)

    def render(
        self,
        request: HttpRequest,
        post: Post,
        formset: Formset,
        preview: PostEditState | None = None,
    ):
        context = self.get_context_data(request, post, formset)

        if preview:
            related_objects = prefetch_posts_feed_related_objects(
                request.settings,
                request.user_permissions,
                [preview.post],
                categories=[post.category],
                threads=[post.thread],
                users=[post.poster],
                attachments=preview.attachments,
            )

            context["preview"] = preview.post.parsed
            context["preview_rich_text_data"] = related_objects

        if self.is_inline(request):
            template_name = self.template_name_inline_form
        elif request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: Formset
    ) -> dict:
        raise NotImplementedError()

    def get_context_data_action(
        self, request: HttpRequest, post: Post, formset: Formset
    ) -> dict:
        return {
            "template_name_htmx": self.template_name_htmx,
            "thread": post.thread,
            "post": post,
            "formset": formset,
        }

    def is_inline(self, request: HttpRequest) -> bool:
        return request.is_htmx and request.GET.get("inline")

    def get_redirect_to_post(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        raise NotImplementedError()


class ThreadPostEditView(EditView, ThreadView):
    template_name: str = "misago/thread_post_edit/index.html"
    template_name_htmx: str = "misago/thread_post_edit/form.html"

    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_edit_thread_post_permission(
            request.user_permissions, post.category, post.thread, post
        )
        return post

    def get_state(self, request: HttpRequest, post: Post) -> ThreadPostEditState:
        return get_thread_post_edit_state(request, post)

    def get_formset(self, request: HttpRequest, post: Post) -> ThreadPostEditFormset:
        return get_thread_post_edit_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: ThreadPostEditFormset
    ) -> dict:
        return get_thread_post_edit_context_data_hook(
            self.get_context_data_action, request, post, formset
        )

    def get_redirect_to_post(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return redirect_to_thread_post(request, thread, post)


class PrivateThreadPostEditView(EditView, PrivateThreadView):
    template_name: str = "misago/private_thread_post_edit/index.html"
    template_name_htmx: str = "misago/private_thread_post_edit/form.html"

    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_edit_private_thread_post_permission(
            request.user_permissions, post.thread, post
        )
        return post

    def get_state(self, request: HttpRequest, post: Post) -> PrivateThreadPostEditState:
        return get_private_thread_post_edit_state(request, post)

    def get_formset(
        self, request: HttpRequest, post: Post
    ) -> PrivateThreadPostEditFormset:
        return get_private_thread_post_edit_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: PrivateThreadPostEditFormset
    ) -> dict:
        return get_private_thread_post_edit_context_data_hook(
            self.get_context_data_action, request, post, formset
        )

    def get_redirect_to_post(
        self, request: HttpRequest, thread: Thread, post: Post
    ) -> HttpResponse:
        return redirect_to_private_thread_post(request, thread, post)


class ThreadEditView(ThreadPostEditView):
    template_name: str = "misago/thread_edit/index.html"
    template_name_htmx: str = "misago/thread_edit/form.html"
    allow_edit_thread: bool = True

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_edit_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_formset(self, request: HttpRequest, post: Post) -> ThreadEditFormset:
        return get_thread_edit_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: ThreadEditFormset
    ) -> dict:
        return get_thread_edit_context_data_hook(
            self.get_context_data_action, request, post, formset
        )


class PrivateThreadEditView(PrivateThreadPostEditView):
    template_name: str = "misago/private_thread_edit/index.html"
    template_name_htmx: str = "misago/private_thread_edit/form.html"
    allow_edit_thread: bool = True

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_edit_private_thread_permission(request.user_permissions, thread)
        return thread

    def get_formset(self, request: HttpRequest, post: Post) -> PrivateThreadEditFormset:
        return get_private_thread_edit_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: PrivateThreadEditFormset
    ) -> dict:
        return get_private_thread_edit_context_data_hook(
            self.get_context_data_action, request, post, formset
        )
