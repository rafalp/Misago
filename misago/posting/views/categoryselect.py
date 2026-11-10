from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import pgettext
from django.views import View

from ...categories.display import get_categories_with_branches
from ...categories.models import Category
from ...permissions.checkutils import check_permissions
from ...permissions.threads import check_start_thread_permission


class ThreadStartCategorySelectView(View):
    template_name = "misago/thread_start_category_select/index.html"
    template_name_htmx = "misago/thread_start_category_select/modal.html"

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

        return render(request, template_name, {"thread_start_choices": choices})

    def get_category_choices(self, request: HttpRequest) -> list[dict]:
        categories = list(
            Category.objects.filter(id__in=request.categories).order_by("lft")
        )
        category_data: dict[int, dict] = {}

        for category in categories:
            with check_permissions() as has_permission:
                check_start_thread_permission(request.user_permissions, category)

            category_data[category.id] = {
                "disabled": category.is_vanilla or not has_permission,
                "url": reverse(
                    "misago:thread-start",
                    kwargs={"category_id": category.id, "slug": category.slug},
                ),
            }

        visible_ids = {
            category.id
            for category in categories
            if not category_data[category.id]["disabled"]
        }
        categories_by_id = {category.id: category for category in categories}

        for category_id in tuple(visible_ids):
            parent_id = categories_by_id[category_id].parent_id
            while parent_id in categories_by_id:
                visible_ids.add(parent_id)
                parent_id = categories_by_id[parent_id].parent_id

        choices: list[dict] = []
        visible_categories = [
            category for category in categories if category.id in visible_ids
        ]
        for branch, category in get_categories_with_branches(visible_categories):
            choices.append(
                {
                    "branch": branch,
                    "category": category,
                    **category_data[category.id],
                }
            )

        return choices
