from typing import Iterable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import pgettext

from ...auth.decorators import login_required
from ...htmx.response import htmx_redirect
from ...permissions.privatethreads import (
    check_edit_private_thread_post_permission,
    check_edit_private_thread_permission,
)
from ...permissions.threads import (
    check_edit_post_permission,
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
    EditPrivateThreadPostState,
    EditThreadPostState,
    get_edit_private_thread_post_state,
    get_edit_thread_post_state,
)
from ..hooks import (
    get_edit_private_thread_post_page_context_data_hook,
    get_edit_thread_post_page_context_data_hook,
)
from ..models import Post, Thread
from .redirect import private_thread_post_redirect, thread_post_redirect
from .generic import PrivateThreadView, ThreadView


def edit_thread_post_login_required():
    return login_required(
        pgettext(
            "post thread page",
            "Sign in to edit posts",
        )
    )


class EditView(View):
    template_name: str
    template_name_htmx: str
    post_select_related: Iterable[str] = ("thread", "category", "poster")

    @method_decorator(edit_thread_post_login_required())
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

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
        formset = self.get_formset(request, post_obj)
        formset.update_state(state)

        if request.POST.get("preview"):
            return self.render(request, post_obj, formset, state.post.parsed)

        if not formset.is_valid():
            return self.render(request, post_obj, formset)

        state.save()

        if post:
            success_message = pgettext("thread post edited", "Post edited")
        else:
            success_message = pgettext("thread edited", "Thread edited")

        messages.success(request, success_message)

        if post:
            redirect_url = self.get_redirect_url(request, state.thread, state.post)
        else:
            redirect_url = self.get_thread_url(thread)

        if request.is_htmx:
            return htmx_redirect(redirect_url)

        return redirect(redirect_url)

    def get_state(self, request: HttpRequest, post: Post) -> EditThreadPostState:
        raise NotImplementedError()

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        raise NotImplementedError()

    def render(
        self,
        request: HttpRequest,
        post: Post,
        formset: PostingFormset,
        preview: str | None = None,
    ):
        context = self.get_context_data(request, post, formset)
        context["preview"] = preview

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        raise NotImplementedError()

    def get_redirect_url(self, request: HttpRequest, thread: Thread, post: Post) -> str:
        raise NotImplementedError()


class ThreadEditPostView(EditView, ThreadView):
    template_name: str = "misago/edit_thread_post/index.html"
    template_name_htmx: str = "misago/edit_thread_post/form.html"

    def get_thread_post(
        self, request: HttpRequest, thread: Thread, post_id: int
    ) -> Post:
        post = super().get_thread_post(request, thread, post_id)
        check_edit_post_permission(
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

    def get_context_data_action(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        return {
            "thread": post.thread,
            "post": post,
            "formset": formset,
            "template_name_htmx": self.template_name_htmx,
        }

    def get_redirect_url(self, request: HttpRequest, thread: Thread, post: Post) -> str:
        return thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )["location"]


class PrivateThreadEditPostView(EditView, PrivateThreadView):
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

    def get_context_data_action(
        self, request: HttpRequest, post: Post, formset: PostingFormset
    ) -> dict:
        return {
            "thread": post.thread,
            "post": post,
            "formset": formset,
            "template_name_htmx": self.template_name_htmx,
        }

    def get_redirect_url(self, request: HttpRequest, thread: Thread, post: Post) -> str:
        return private_thread_post_redirect(
            request, id=thread.id, slug=thread.slug, post=post.id
        )["location"]


class ThreadEditView(ThreadEditPostView):
    template_name: str = "misago/edit_thread/index.html"
    template_name_htmx: str = "misago/edit_thread/form.html"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_edit_thread_permission(request.user_permissions, thread.category, thread)
        return thread

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        return get_edit_thread_formset(request, post.thread, post)


class PrivateThreadEditView(PrivateThreadEditPostView):
    template_name: str = "misago/edit_private_thread/index.html"
    template_name_htmx: str = "misago/edit_private_thread/form.html"

    def get_thread(self, request: HttpRequest, thread_id: int) -> Thread:
        thread = super().get_thread(request, thread_id)
        check_edit_private_thread_permission(request.user_permissions, thread)
        return thread

    def get_formset(self, request: HttpRequest, post: Post) -> PostingFormset:
        return get_edit_private_thread_formset(request, post.thread, post)


thread_edit = ThreadEditView.as_view()
private_thread_edit = PrivateThreadEditView.as_view()
thread_edit_post = ThreadEditPostView.as_view()
private_thread_edit_post = PrivateThreadEditPostView.as_view()
