from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import pgettext

from ...auth.decorators import login_required
from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...permissions.categories import check_browse_category_permission
from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_start_private_threads_permission,
)
from ...permissions.threads import check_start_thread_permission
from ...posting.formsets import (
    PostingFormset,
    StartPrivateThreadFormset,
    StartThreadFormset,
    get_start_private_thread_formset,
    get_start_thread_formset,
)
from ...posting.state.start import (
    StartPrivateThreadState,
    StartThreadState,
    get_start_private_thread_state,
    get_start_thread_state,
)
from ...posting.validators import validate_flood_control, validate_posted_contents
from ..hooks import (
    get_start_private_thread_page_context_data_hook,
    get_start_thread_page_context_data_hook,
)
from ..models import Thread
from ..prefetch import prefetch_posts_related_objects


class StartThreadView(View):
    template_name: str = "misago/start_thread/index.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs)
        formset = self.get_formset(request, category)

        return render(
            request,
            self.template_name,
            self.get_context_data(request, category, formset),
        )

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs)
        state = self.get_state(request, category)
        formset = self.get_formset(request, category)
        formset.update_state(state)

        if formset.is_request_preview(request):
            formset.clear_errors_in_preview()
            return self.preview(request, category, formset, state)

        if formset.is_request_upload(request):
            context = self.get_context_data(request, category, formset)
            formset.clear_errors_in_upload()
            return render(request, self.template_name, context)

        if not self.is_valid(formset, state):
            return render(
                request,
                self.template_name,
                self.get_context_data(request, category, formset),
            )

        state.save()

        messages.success(request, pgettext("thread started", "Thread started"))

        thread_url = self.get_thread_url(request, state.thread)
        return redirect(thread_url)

    def preview(
        self,
        request: HttpRequest,
        category: Category,
        formset: StartThreadFormset,
        state: StartThreadState,
    ) -> HttpResponse:
        formset.clear_errors_in_preview()

        context = self.get_context_data(request, category, formset)

        related_objects = prefetch_posts_related_objects(
            request.settings,
            request.user_permissions,
            [state.post],
            categories=[category],
            attachments=state.attachments,
        )

        context["preview"] = state.post.parsed
        context["preview_rich_text_data"] = related_objects

        return render(request, self.template_name, context)

    def get_category(self, request: HttpRequest, kwargs: dict) -> Category:
        try:
            category = Category.objects.get(
                id=kwargs["id"],
                tree_id=CategoryTree.THREADS,
                level__gt=0,
            )
        except Category.DoesNotExist:
            raise Http404()

        check_browse_category_permission(
            request.user_permissions, category, can_delay=True
        )
        check_start_thread_permission(request.user_permissions, category)

        return category

    def get_formset(
        self, request: HttpRequest, category: Category
    ) -> StartThreadFormset:
        return get_start_thread_formset(request, category)

    def get_state(self, request: HttpRequest, category: Category) -> StartThreadState:
        return get_start_thread_state(request, category)

    def is_valid(self, formset: StartThreadFormset, state: StartThreadState) -> bool:
        return (
            formset.is_valid()
            and validate_flood_control(formset, state)
            and validate_posted_contents(formset, state)
        )

    def get_context_data(
        self, request: HttpRequest, category: Category, formset: StartThreadFormset
    ) -> dict:
        return get_start_thread_page_context_data_hook(
            self.get_context_data_action, request, category, formset
        )

    def get_context_data_action(
        self, request: HttpRequest, category: Category, formset: PostingFormset
    ) -> dict:
        return {"category": category, "formset": formset}

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )


class StartPrivateThreadView(StartThreadView):
    template_name: str = "misago/start_private_thread/index.html"

    def get_category(self, request: HttpRequest, kwargs: dict) -> Category:
        check_private_threads_permission(request.user_permissions)
        check_start_private_threads_permission(request.user_permissions)
        return Category.objects.private_threads()

    def get_formset(
        self, request: HttpRequest, category: Category
    ) -> StartPrivateThreadFormset:
        return get_start_private_thread_formset(request, category)

    def get_state(
        self, request: HttpRequest, category: Category
    ) -> StartPrivateThreadState:
        return get_start_private_thread_state(request, category)

    def get_context_data(
        self,
        request: HttpRequest,
        category: Category,
        formset: StartPrivateThreadFormset,
    ) -> dict:
        return get_start_private_thread_page_context_data_hook(
            self.get_context_data_action, request, category, formset
        )

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:private-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )


def start_thread_login_required(f):
    return login_required(
        pgettext(
            "start thread page",
            "Sign in to start new thread",
        )
    )(f)


start_thread = start_thread_login_required(StartThreadView.as_view())
start_private_thread = start_thread_login_required(StartPrivateThreadView.as_view())
