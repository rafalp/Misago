from typing import Any
from django.http import Http404, HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...pagination.cursor import paginate_queryset
from ...permissions.categories import (
    check_browse_category_permission,
    filter_categories_threads_queryset,
)
from ...permissions.private_threads import check_private_threads_permission
from ..models import Thread


class ListView(View):
    template_name: str

    def get(self, request: HttpRequest, **kwargs):
        context = self.get_context(request, kwargs)
        return render(request, self.template_name, context)

    def get_context(self, request: HttpRequest, kwargs: dict):
        return {"request": request}


class ThreadsListView(ListView):
    template_name = "misago/threads/index.html"

    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        is_index: bool | None = None,
        **kwargs: Any
    ) -> HttpResponse:
        if not is_index and request.settings.index_view == "threads":
            return redirect(reverse("misago:index"))

        return super().dispatch(request, *args, is_index=is_index, **kwargs)

    def get_context(self, request: HttpRequest, kwargs: dict):
        threads = self.get_threads(request, kwargs)

        return {
            "request": request,
            "is_index": kwargs.get("is_index", False),
            "threads": threads,
        }

    def get_threads(self, request: HttpRequest, kwargs: dict):
        categories: list[int] = list(request.categories.categories)
        queryset = filter_categories_threads_queryset(
            request.user_permissions,
            categories,
            Thread.objects,
        )

        paginator = paginate_queryset(
            request,
            queryset,
            request.settings.threads_per_page,
            order_by="-last_post_id",
            raise_404=True,
        )

        return {
            "items": paginator.items,
            "paginator": paginator,
        }


class CategoryThreadsListView(ListView):
    template_name = "misago/category/index.html"

    def get_context(self, request: HttpRequest, kwargs: dict):
        category = self.get_category(request, kwargs)

        if not (category.is_vanilla and category.list_children_threads):
            threads = self.get_threads(request, category, kwargs)
        else:
            threads = None

        path = request.categories.get_category_path(category.id, include_self=False)

        return {
            "request": request,
            "category": category,
            "threads": threads,
            "breadcrumbs": path,
        }

    def get_category(self, request: HttpRequest, kwargs: dict):
        try:
            category = Category.objects.get(
                id=kwargs["id"],
                tree_id=CategoryTree.THREADS,
                level__gt=0,
            )
        except Category.DoesNotExist:
            raise Http404()

        check_browse_category_permission(
            request.user_permissions,
            category,
            delay_browse_check=True,
        )

        return category

    def get_threads(self, request: HttpRequest, category: Category, kwargs: dict):
        categories: list[int] = []
        if category.list_children_threads:
            categories += [
                c["id"]
                for c in request.categories.get_category_descendants(category.id)
            ]
        else:
            categories.append(category.id)

        queryset = filter_categories_threads_queryset(
            request.user_permissions,
            categories,
            Thread.objects,
        )

        paginator = paginate_queryset(
            request,
            queryset,
            request.settings.threads_per_page,
            order_by="-last_post_id",
            raise_404=True,
        )

        return {
            "items": paginator.items,
            "paginator": paginator,
        }

    def get_threads_queryset(
        self, request: HttpRequest, category: Category, kwargs: dict
    ):
        pass

    def get_pinned_threads_queryset(
        self, request: HttpRequest, category: Category, kwargs: dict, queryset
    ):
        pass

    def get_pinned_threads_queryset(
        self, request: HttpRequest, category: Category, kwargs: dict, queryset
    ):
        pass


class PrivateThreadsListView(ListView):
    template_name = "misago/private_threads/index.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        check_private_threads_permission(request.user_permissions)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, **kwargs):
        context = self.get_context(request, kwargs)
        return render(request, self.template_name, context)


threads = ThreadsListView.as_view()
category_threads = CategoryThreadsListView.as_view()
private_threads = PrivateThreadsListView.as_view()
