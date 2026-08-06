from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import pgettext
from django.views import View

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...notifications.tasks import notify_on_new_private_thread
from ...notifications.threads import watch_started_thread
from ...permissions.categories import check_browse_category_permission
from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_start_private_threads_permission,
)
from ...permissions.threads import check_start_thread_permission
from ...privatethreads.threadtypes import private_thread_type
from ...threads.prefetch import prefetch_post_feed_data
from ...threads.threadtypes import thread_type
from ...threads.views import BaseThreadView
from ..formsets import (
    Formset,
    PrivateThreadStartFormset,
    TabbedFormset,
    ThreadStartFormset,
    get_private_thread_start_formset,
    get_thread_start_formset,
)
from ..state.start import (
    PrivateThreadStartState,
    StartState,
    ThreadStartState,
    get_private_thread_start_state,
    get_thread_start_state,
)
from ..validators import validate_flood_control, validate_posted_contents


class StartView(BaseThreadView):
    template_name: str

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

        self.post_state_save(request, state, formset)

        messages.success(request, pgettext("thread started", "Thread started"))

        thread_url = self.get_thread_url(state.thread)
        return redirect(thread_url)

    def preview(
        self,
        request: HttpRequest,
        category: Category,
        formset: Formset | TabbedFormset,
        state: StartState,
    ) -> HttpResponse:
        formset.clear_errors_in_preview()

        context = self.get_context_data(request, category, formset)

        related_objects = prefetch_post_feed_data(
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
        raise NotImplementedError()

    def get_formset(
        self, request: HttpRequest, category: Category
    ) -> Formset | TabbedFormset:
        raise NotImplementedError()

    def get_state(self, request: HttpRequest, category: Category) -> StartState:
        raise NotImplementedError()

    def is_valid(self, formset: Formset | TabbedFormset, state: StartState) -> bool:
        return (
            formset.is_valid()
            and validate_flood_control(formset, state)
            and validate_posted_contents(formset, state)
        )

    def post_state_save(
        self, request: HttpRequest, state: StartState, formset: Formset | TabbedFormset
    ):
        formset.save(state)

        watch_started_thread(state.thread, state.user, request)

    def get_context_data(
        self, request: HttpRequest, category: Category, formset: Formset | TabbedFormset
    ) -> dict:
        return {
            "category": category,
            "formset": formset,
            "breadcrumbs": self.get_category_breadcrumbs(request, category),
        }


class ThreadStartView(StartView):
    thread_type = thread_type

    template_name: str = "misago/thread_start/index.html"

    def get_category(self, request: HttpRequest, kwargs: dict) -> Category:
        try:
            category = Category.objects.get(
                id=kwargs["category_id"],
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
    ) -> ThreadStartFormset:
        return get_thread_start_formset(request, category)

    def get_state(self, request: HttpRequest, category: Category) -> ThreadStartState:
        return get_thread_start_state(request, category)


class PrivateThreadStartView(StartView):
    thread_type = private_thread_type

    template_name: str = "misago/private_thread_start/index.html"

    def get_category(self, request: HttpRequest, kwargs: dict) -> Category:
        check_private_threads_permission(request.user_permissions)
        check_start_private_threads_permission(request.user_permissions)
        return Category.objects.private_threads()

    def get_formset(
        self, request: HttpRequest, category: Category
    ) -> PrivateThreadStartFormset:
        return get_private_thread_start_formset(request, category)

    def get_state(
        self, request: HttpRequest, category: Category
    ) -> PrivateThreadStartState:
        return get_private_thread_start_state(request, category)

    def post_state_save(
        self,
        request: HttpRequest,
        state: PrivateThreadStartState,
        formset: PrivateThreadStartFormset,
    ):
        super().post_state_save(request, state, formset)

        notify_on_new_private_thread.delay(
            state.thread.starter_id,
            state.thread.id,
            [user.id for user in state.members],
        )
