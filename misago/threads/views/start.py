from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
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
    StartPrivateThreadFormset,
    StartThreadFormset,
    get_start_private_thread_formset,
    get_start_thread_formset,
)
from ...posting.hooks import (
    get_start_private_thread_page_context_data_hook,
    get_start_thread_page_context_data_hook,
)
from ...posting.state.start import (
    StartPrivateThreadState,
    StartThreadState,
    get_start_private_thread_state,
    get_start_thread_state,
)
from ..models import Thread


def start_thread_login_required():
    return login_required(
        pgettext(
            "start thread page",
            "Sign in to start new thread",
        )
    )


class StartThreadView(View):
    template_name: str = "misago/start_thread/index.html"
    state_class = StartThreadState

    @method_decorator(start_thread_login_required())
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

        if request.POST.get("preview"):
            context = self.get_context_data(request, category, formset)
            context["preview"] = state.post.parsed

            return render(request, self.template_name, context)

        if not formset.is_valid():
            return render(
                request,
                self.template_name,
                self.get_context_data(request, category, formset),
            )

        state.save()
        thread_url = self.get_thread_url(request, state.thread)
        return redirect(thread_url)

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

    def get_context_data(
        self, request: HttpRequest, category: Category, formset: StartThreadFormset
    ) -> dict:
        return get_start_thread_page_context_data_hook(
            self.get_context_data_action, request, category, formset
        )

    def get_context_data_action(
        self, request: HttpRequest, category: Category, formset: StartThreadFormset
    ) -> dict:
        return {"category": category, "formset": formset}

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )


class StartPrivateThreadView(StartThreadView):
    template_name: str = "misago/start_private_thread/index.html"
    state_class = StartPrivateThreadState

    def get_category(self, request: HttpRequest, kwargs: dict) -> Category:
        check_private_threads_permission(request.user_permissions)
        check_start_private_threads_permission(request.user_permissions)
        return Category.objects.private_threads()

    def get_formset(
        self, request: HttpRequest, category: Category
    ) -> StartPrivateThreadFormset:
        return get_start_private_thread_formset(request, category)

    def get_state(self, request: HttpRequest, category: Category) -> StartThreadState:
        return get_start_private_thread_state(request, category)

    def get_context_data(
        self, request: HttpRequest, category: Category, formset: StartThreadFormset
    ) -> dict:
        return get_start_private_thread_page_context_data_hook(
            self.get_context_data_action, request, category, formset
        )

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:private-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
