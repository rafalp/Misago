from django.http import HttpRequest
from django.views import View
from django.shortcuts import render

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...pagination.cursor import paginate_queryset
from ...permissions.categories import (
    check_category_browse_permission,
    filter_categories_threads_queryset,
)
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

    def get_context(self, request: HttpRequest, kwargs: dict):
        threads = self.get_threads(request, kwargs)

        return {
            "request": request,
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

        return {
            "request": request,
            "category": category,
            "threads": threads,
        }

    def get_category(self, request: HttpRequest, kwargs: dict):
        category = Category.objects.get(
            id=kwargs["id"],
            tree_id=CategoryTree.THREADS,
            level__gt=0,
        )

        check_category_browse_permission(
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
    pass
