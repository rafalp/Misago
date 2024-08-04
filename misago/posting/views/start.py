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
from ...permissions.enums import CategoryPermission
from ...permissions.categories import check_browse_category_permission
from ...threads.models import Thread
from ..forms.start import ThreadStartForm
from ..states.start import StartState, StartThreadState


def start_thread_login_required():
    return login_required(
        pgettext(
            "start thread page",
            "Sign in to start new thread",
        )
    )


class StartView(View):
    template_name: str
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

    def get_form(self, request: HttpRequest, category: Category) -> Form:
        if request.method == "POST":
            return self.form_class(request.POST, request.FILES)

        return self.form_class()

    def get_state(self, request: HttpRequest, category: Category) -> StartState:
        return self.state_class(request, category)

    def get_context_data(
        self, request: HttpRequest, category: Category, form: Form
    ) -> dict:
        return {"category": category, "form": form}

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        raise NotImplementedError()


class ThreadStartView(StartView):
    template_name: str = "misago/posting/start.html"

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

    def get_thread_url(self, request: HttpRequest, thread: Thread) -> str:
        return reverse(
            "misago:thread",
            kwargs={"pk": thread.id, "slug": thread.slug},
        )


class PrivateThreadStartView(StartView):
    pass


class ThreadStartSelectCategoryView(View):
    template_name = "misago/posting/select_category_page.html"
    template_name_htmx = "misago/posting/select_category_modal.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        context = self.get_context_data(request)

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        if not context["start_thread_choices"] and not request.is_htmx:
            raise PermissionDenied(
                pgettext(
                    "start thread page",
                    "You can't start new threads.",
                )
            )

        return render(request, template_name, context)

    def get_context_data(self, request: HttpRequest) -> dict:
        permissions = request.user_permissions.categories[CategoryPermission.START]

        choices: list[dict] = []
        for category in request.categories.categories_list:
            choice = {
                "id": category["id"],
                "name": category["name"],
                "short_name": category["short_name"],
                "color": category["color"],
                "level": "",
                "is_vanilla": category["is_vanilla"],
                "disabled": (
                    category["is_vanilla"] or category["id"] not in permissions
                ),
            }

            if not category["level"]:
                choice["children"] = []
                choices.append(choice)
            else:
                parent = choices[-1]
                choice["level"] = "1" * (category["level"] - 1)
                parent["children"].append(choice)

        choices_dict: dict[int, dict] = {}

        # Remove branches where entire branch is disabled
        clean_choices: list[dict] = []
        for category in choices:
            clean_children: list[dict] = []
            for child in reversed(category["children"]):
                if not child["disabled"] or (
                    clean_children and clean_children[-1]["level"] > child["level"]
                ):
                    choices_dict[child["id"]] = child
                    clean_children.append(child)

            if not category["disabled"] or clean_children:
                choices_dict[category["id"]] = category
                category["children"] = reversed(clean_children)
                clean_choices.append(category)

        # Populate choices with full category instances
        for category in Category.objects.filter(id__in=choices_dict):
            choices_dict[category.id]["url"] = reverse(
                "misago:start-thread",
                kwargs={"id": category.id, "slug": category.slug},
            )
            choices_dict[category.id]["category"] = category
            choices_dict[category.id]["description"] = category.description

        return {"start_thread_choices": clean_choices}
