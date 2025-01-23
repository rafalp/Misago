from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import pgettext

from ...categories.models import Category
from ...permissions.checkutils import check_permissions
from ...permissions.threads import check_start_thread_permission


class SelectCategoryView(View):
    template_name = "misago/select_category/page.html"
    template_name_htmx = "misago/select_category/modal.html"

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
            with check_permissions() as has_permission:
                check_start_thread_permission(request.user_permissions, category)

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
                category["children"] = list(reversed(clean_children))
                clean_choices.append(category)

        return clean_choices
