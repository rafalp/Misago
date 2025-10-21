from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import pgettext

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...notifications.tasks import notify_on_new_private_thread
from ...permissions.categories import check_browse_category_permission
from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_start_private_threads_permission,
)
from ...permissions.threads import check_start_thread_permission
from ...threads.models import Thread
from ...threads.prefetch import prefetch_posts_feed_related_objects
from ..formsets import (
    Formset,
    PrivateThreadStartFormset,
    TabbedFormset,
    ThreadStartFormset,
    get_private_thread_start_formset,
    get_thread_start_formset,
)
from ..hooks import (
    get_private_thread_start_context_data_hook,
    get_thread_start_context_data_hook,
)
from ..state.start import (
    PrivateThreadStartState,
    StartState,
    ThreadStartState,
    get_private_thread_start_state,
    get_thread_start_state,
)
from ..validators import validate_flood_control, validate_posted_contents


class StartView(View):
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

        self.post_state_save(request, state)

        messages.success(request, pgettext("thread started", "Thread started"))

        thread_url = self.get_thread_url(request, state.thread)
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

        related_objects = prefetch_posts_feed_related_objects(
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

    def post_state_save(self, request: HttpRequest, state: StartState):
        pass

    def get_context_data(
        self, request: HttpRequest, category: Category, formset: Formset | TabbedFormset
    ) -> dict:
        return self.get_context_data_action(request, category, formset)

    def get_context_data_action(
        self, request: HttpRequest, category: Category, formset: Formset | TabbedFormset
    ) -> dict:
        return {"category": category, "formset": formset}


class ThreadStartView(StartView):
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

    def get_context_data(
        self, request: HttpRequest, category: Category, formset: ThreadStartFormset
    ) -> dict:
        return get_thread_start_context_data_hook(
            self.get_context_data_action, request, category, formset
        )

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )


class PrivateThreadStartView(StartView):
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

    def get_context_data(
        self,
        request: HttpRequest,
        category: Category,
        formset: PrivateThreadStartFormset,
    ) -> dict:
        return get_private_thread_start_context_data_hook(
            self.get_context_data_action, request, category, formset
        )

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:private-thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )

    def post_state_save(self, request: HttpRequest, state: PrivateThreadStartState):
        notify_on_new_private_thread.delay(
            state.thread.starter_id,
            state.thread.id,
            [user.id for user in state.members],
        )
