from django.core.exceptions import PermissionDenied
from django.forms import Form
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
from ...permissions.threads import check_start_thread_in_category_permission
from ...threads.models import Thread
from ..forms.start import ThreadStartForm
from ..states.start import StartPrivateThreadState, StartThreadState


def start_thread_login_required():
    return login_required(
        pgettext(
            "start thread page",
            "Sign in to start new thread",
        )
    )


class ThreadStartView(View):
    template_name: str = "misago/posting/start.html"
    form_class = ThreadStartForm
    state_class = StartThreadState

    @method_decorator(start_thread_login_required())
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs["id"])
        form = self.get_form(request, category)

        return render(
            request,
            self.template_name,
            self.get_context_data(request, category, form),
        )

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        category = self.get_category(request, kwargs["id"])
        state = self.get_state(request, category)
        form = self.get_form(request, category)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self.get_context_data(request, category, form),
            )

        form.update_state(state)

        if request.POST.get("preview"):
            context = self.get_context_data(request, category, form)
            context["preview"] = state.post.html

            return render(request, self.template_name, context)

        state.save()
        thread_url = self.get_thread_url(request, state.thread)
        return redirect(thread_url)

    def get_category(self, request: HttpRequest, category_id: int) -> Category:
        try:
            category = Category.objects.get(
                id=category_id,
                tree_id=CategoryTree.THREADS,
                level__gt=0,
            )
        except Category.DoesNotExist:
            raise Http404()

        check_browse_category_permission(
            request.user_permissions, category, can_delay=True
        )

        return category

    def get_form(self, request: HttpRequest, category: Category) -> Form:
        if request.method == "POST":
            return self.form_class(request.POST, request.FILES)

        return self.form_class()

    def get_state(self, request: HttpRequest, category: Category) -> StartThreadState:
        return self.state_class(request, category)

    def get_context_data(
        self, request: HttpRequest, category: Category, form: Form
    ) -> dict:
        return {"category": category, "form": form}

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:thread",
            kwargs={"pk": thread.id, "slug": thread.slug},
        )


class PrivateThreadStartView(ThreadStartView):
    state_class = StartPrivateThreadState


class ThreadStartSelectCategoryView(View):
    template_name = "misago/posting/select_category_page.html"
    template_name_htmx = "misago/posting/select_category_modal.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        choices = self.get_category_choices(request)

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        if not choices and not request.is_htmx:
            raise PermissionDenied(
                pgettext(
                    "start thread page",
                    "You can't start new threads.",
                )
            )

        return render(request, template_name, {"start_thread_choices": choices})

    def get_category_choices(self, request: HttpRequest) -> list[dict]:
        queryset = Category.objects.filter(
            id__in=list(request.categories.categories),
        ).order_by("lft")

        choices: list[dict] = []
        for category in queryset:
            try:
                check_start_thread_in_category_permission(
                    request.user_permissions, category
                )
            except (Http404, PermissionDenied):
                has_permission = False
            else:
                has_permission = True

            choice = {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "color": category.color,
                "level": "",
                "is_vanilla": category.is_vanilla,
                "disabled": category.is_vanilla or not has_permission,
                "url": reverse(
                    "misago:start-thread",
                    kwargs={"id": category.id, "slug": category.slug},
                ),
                "category": category,
            }

            if category.level == 1:
                choice["children"] = []
                choices.append(choice)
            else:
                parent = choices[-1]
                choice["level"] = "1" * (category.level - 1)
                parent["children"].append(choice)

        # Remove branches where entire branch is disabled
        clean_choices: list[dict] = []
        for category in choices:
            clean_children: list[dict] = []
            for child in reversed(category["children"]):
                if not child["disabled"] or (
                    clean_children and clean_children[-1]["level"] > child["level"]
                ):
                    clean_children.append(child)

            if not category["disabled"] or clean_children:
                category["children"] = reversed(clean_children)
                clean_choices.append(category)

        return clean_choices
