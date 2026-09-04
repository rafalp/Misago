from datetime import datetime, time, timedelta

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import pgettext
from django.views import View

from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..categories.proxy import CategoryProxy
from ..permissions.checkutils import check_permissions
from ..permissions.enums import CategoryPermission
from ..permissions.privatethreads import check_private_threads_permission
from ..permissions.search import check_search_permission
from ..plugins import extensions
from .categories import get_searchable_category_ids
from .enums import SearchSort
from .forms import (
    PrivateThreadsSearchForm,
    SearchForm,
    ThreadsSearchForm,
    UsersSearchForm,
)
from .posts import posts_search


class SearchView(View):
    template_name = "misago/search/index.html"
    header_template_name = "misago/search/header.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        self.check_permission()
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def check_permission(self):
        check_search_permission(self.request.user_permissions)

    def get_context_data(self):
        search_forms = self.get_search_forms()

        return {
            "header": self.get_header_data(),
            "search_forms": search_forms,
        }

    def get_header_data(self) -> dict:
        return {"template_name": self.header_template_name}

    def get_search_forms(self) -> list[SearchForm]:
        forms = []

        if threads_search_form := self.get_threads_search_form():
            forms.append(threads_search_form)

        if private_threads_form := self.get_private_threads_search_form():
            forms.append(private_threads_form)

        if users_form := self.get_users_search_form():
            forms.append(users_form)

        if not forms:
            raise PermissionDenied(
                pgettext(
                    "search permission error",
                    "You can't search this site.",
                )
            )

        return forms

    def get_threads_search_form(self) -> ThreadsSearchForm:
        request = self.request

        searchable_categories = get_searchable_category_ids(
            request.user_permissions, request.categories
        )

        if searchable_categories:
            form_class = extensions.get(ThreadsSearchForm)
            return form_class(request=self.request)

    def get_private_threads_search_form(self) -> PrivateThreadsSearchForm | None:
        with check_permissions():
            check_private_threads_permission(self.request.user_permissions)
            form_class = extensions.get(PrivateThreadsSearchForm)
            return form_class(request=self.request)

    def get_users_search_form(self) -> UsersSearchForm | None:
        form_class = extensions.get(UsersSearchForm)
        return form_class(request=self.request)


class BaseSearchView(View):
    breadcrumbs_template_name = "misago/search/breadcrumbs.html"

    def get_breadcrumbs(self):
        return {
            "id": "breadcrumbs",
            "template_name": self.breadcrumbs_template_name,
        }


class ThreadsSearchView(BaseSearchView):
    template_name = "misago/search/threads/index.html"
    header_template_name = "misago/search/threads/header.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        self.check_permission()
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def check_permission(self):
        check_search_permission(self.request.user_permissions)

    def get_context_data(self) -> dict:
        form = self.get_search_form()

        if form.is_valid():
            results = self.get_results_data(form)
        else:
            results = None

        return {
            "page_title": form.name,
            "breadcrumbs": self.get_breadcrumbs(),
            "header": self.get_header_data(),
            "form": form,
            "results": results,
        }

    def get_search_form(self) -> ThreadsSearchForm:
        form_class = extensions.get(ThreadsSearchForm)
        return form_class(self.request.GET, request=self.request)

    def get_header_data(self) -> dict:
        return {"template_name": self.header_template_name}

    def get_results_data(self, form: ThreadsSearchForm) -> dict:
        request = self.request

        filters = form.cleaned_data

        query = filters["query"]
        mode = filters["mode"]
        sort = filters["sort"]

        categories = self.get_categories_filter(filters)
        users = filters.get("users")
        date_from = None
        date_to = None

        if date_from := filters.get("date_from"):
            date_from = timezone.make_aware(datetime.combine(date_from, time.min))
        if date_to := filters.get("date_to"):
            date_to = timezone.make_aware(
                datetime.combine(date_to + timedelta(days=1), time.min)
            )

        if mode == "threads":
            results = posts_search.search_threads(
                query,
                request.user_permissions,
                categories=categories,
                users=users,
                posted_after=date_from,
                posted_before=date_to,
                order_by=SearchSort(sort),
            )
        elif mode == "posts":
            results = posts_search.search_posts(
                query,
                request.user_permissions,
                categories=categories,
                users=users,
                posted_after=date_from,
                posted_before=date_to,
                order_by=SearchSort(sort),
            )
        elif mode == "thread_titles":
            results = posts_search.search_thread_titles(
                query,
                request.user_permissions,
                categories=categories,
                users=users,
                started_after=date_from,
                started_before=date_to,
                order_by=SearchSort(sort),
            )

        return {
            "results": results,
            "more_url": None,
        }

    def get_categories_filter(self, filters: dict) -> list[Category | CategoryProxy]:
        request = self.request

        searchable_categories = get_searchable_category_ids(
            request.user_permissions, request.categories
        )

        if category_ids := filters.get("categories"):
            return [
                request.categories[category_id]
                for category_id in category_ids
                if category_id in searchable_categories
            ]

        return [
            category
            for category in request.categories.values()
            if category.id in searchable_categories
        ]


class PrivateThreadsSearchView(ThreadsSearchView):
    def get_categories_filter(self, filters: dict) -> list[Category]:
        return [Category.objects.filter(tree_id=CategoryTree.PRIVATE_THREADS)]


class UsersSearchView(BaseSearchView):
    pass
