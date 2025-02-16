from typing import Iterable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.utils.translation import pgettext

from ...auth.decorators import login_required
from ...htmx.response import htmx_redirect
from ...permissions.privatethreads import (
    check_edit_private_thread_post_permission,
    check_edit_private_thread_permission,
)
from ...permissions.threads import (
    check_edit_thread_post_permission,
    check_edit_thread_permission,
)
from ...posting.formsets import (
    PostingFormset,
    get_edit_private_thread_formset,
    get_edit_private_thread_post_formset,
    get_edit_thread_formset,
    get_edit_thread_post_formset,
)
from ...posting.state import (
    PostingState,
    EditPrivateThreadPostState,
    EditThreadPostState,
    get_edit_private_thread_post_state,
    get_edit_thread_post_state,
)
from ...posting.validators import validate_posted_contents
from ..hooks import (
    get_edit_private_thread_page_context_data_hook,
    get_edit_private_thread_post_page_context_data_hook,
    get_edit_thread_page_context_data_hook,
    get_edit_thread_post_page_context_data_hook,
)
from ..models import Post, Thread
from ..prefetch import prefetch_posts_related_objects
from .redirect import private_thread_post_redirect, thread_post_redirect
from .generic import PrivateThreadView, ThreadView


class EditView(View):
    template_name: str
    template_name_htmx: str
    template_name_inline: str = "misago/inline_edit/index.html"
    template_name_inline_form: str = "misago/inline_edit/form.html"
    post_select_related: Iterable[str] = ("poster",)
    allow_edit_thread: bool = False

    def get(
        self, request: HttpRequest, id: int, slug: str, post: int | None = None
    ) -> HttpResponse:
        thread = self.get_thread(request, id)
        post_obj = self.get_thread_post(request, thread, post or thread.first_post_id)
        formset = self.get_formset(request, post_obj)
        return self.render(request, post_obj, formset)

    def post(
        self, request: HttpRequest, id: int, slug: str, post: int | None = None
    ) -> HttpResponse:
        thread = self.get_thread(request, id)
        post_obj = self.get_thread_post(request, thread, post or thread.first_post_id)
        state = self.get_state(request, post_obj)

        # Short-circuit post handler if "cancel" button was pressed
        if self.is_inline(request) and request.POST.get("cancel"):
            return self.post_inline_edit(request, state, animate=False)

        formset = self.get_formset(request, post_obj)
        formset.update_state(state)

        if formset.is_request_preview(request):
            formset.clear_errors_in_preview()
            return self.render(request, post_obj, formset, state)

        if formset.is_request_upload(request):
            formset.clear_errors_in_upload()
            return self.render(request, post_obj, formset)

        if not self.is_valid(formset, state):
            return self.render(request, post_obj, formset)

        state.save()

        if post:
            success_message = pgettext("thread post edited", "Post edited")
        else:
            success_message = pgettext("thread edited", "Thread edited")

        messages.success(request, success_message)

        if post and self.is_inline(request):
            return self.post_inline_edit(request, state)

        if post:
            redirect_url = self.get_redirect_url(request, state.thread, state.post)
        else:
            redirect_url = self.get_thread_url(thread)

        if request.is_htmx:
            return htmx_redirect(redirect_url)

        return redirect(redirect_url)

    def post_inline_edit(
        self, request: HttpRequest, state: EditThreadPostState, animate: bool = True
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
        return render(request, self.template_name_inline, context=post_context)

    def get_state(self, request: HttpRequest, post: Post) -> EditThreadPostState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        raise NotImplementedError()

    def is_valid(self, formset: PostingFormset, state: PostingState) -> bool:
        return formset.is_valid() and validate_posted_contents(formset, state)

    def render(
        self,
        request: HttpRequest,
        post: Post,
        formset: PostingFormset,
        preview: PostingState | None = None,
    ):
        context = self.get_context_data(request, post, formset)

        if preview:
            related_objects = prefetch_posts_related_objects(
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
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        raise NotImplementedError()

    def get_context_data_action(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        return {
            "template_name_htmx": self.template_name_htmx,
            "thread": post.thread,
            "post": post,
            "formset": formset,
        }

    def is_inline(self, request: HttpRequest) -> bool:
        return request.is_htmx and request.GET.get("inline")

    def get_redirect_url(self, request: HttpRequest, thread: Thread, post: Post) -> str:
        raise NotImplementedError()


class EditThreadPostView(EditView, ThreadView):
    template_name: str = "misago/edit_thread_post/index.html"
    template_name_htmx: str = "misago/edit_thread_post/form.html"

    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_edit_thread_post_permission(
            request.user_permissions, post.category, post.thread, post
        )
        return post

    def get_state(self, request: HttpRequest, post: Post) -> EditThreadPostState:
        return get_edit_thread_post_state(request, post)

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        return get_edit_thread_post_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        return get_edit_thread_post_page_context_data_hook(
            self.get_context_data_action, request, post, formset
        )

    def get_redirect_url(self, request: HttpRequest, thread: Thread, post: Post) -> str:
        return thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )["location"]


class EditPrivateThreadPostView(EditView, PrivateThreadView):
    template_name: str = "misago/edit_private_thread_post/index.html"
    template_name_htmx: str = "misago/edit_private_thread_post/form.html"

    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_edit_private_thread_post_permission(
            request.user_permissions, post.thread, post
        )
        return post

    def get_state(self, request: HttpRequest, post: Post) -> EditPrivateThreadPostState:
        return get_edit_private_thread_post_state(request, post)

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        return get_edit_private_thread_post_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        return get_edit_private_thread_post_page_context_data_hook(
            self.get_context_data_action, request, post, formset
        )

    def get_redirect_url(self, request: HttpRequest, thread: Thread, post: Post) -> str:
        return private_thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )["location"]


class EditThreadView(EditThreadPostView):
    template_name: str = "misago/edit_thread/index.html"
    template_name_htmx: str = "misago/edit_thread/form.html"
    allow_edit_thread: bool = True

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_edit_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        return get_edit_thread_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        return get_edit_thread_page_context_data_hook(
            self.get_context_data_action, request, post, formset
        )


class EditPrivateThreadView(EditPrivateThreadPostView):
    template_name: str = "misago/edit_private_thread/index.html"
    template_name_htmx: str = "misago/edit_private_thread/form.html"
    allow_edit_thread: bool = True

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_edit_private_thread_permission(request.user_permissions, thread)
        return thread

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        return get_edit_private_thread_formset(request, post)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        return get_edit_private_thread_page_context_data_hook(
            self.get_context_data_action, request, post, formset
        )


def edit_thread_login_required(f):
    return login_required(
        pgettext(
            "edit thread page",
            "Sign in to edit posts",
        )
    )(f)


edit_thread = edit_thread_login_required(EditThreadView.as_view())
edit_private_thread = edit_thread_login_required(EditPrivateThreadView.as_view())
edit_thread_post = edit_thread_login_required(EditThreadPostView.as_view())
edit_private_thread_post = edit_thread_login_required(
    EditPrivateThreadPostView.as_view()
)
