from datetime import datetime, time, timedelta

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import pgettext
from django.views import View

from ..permissions.checkutils import check_permissions
from ..permissions.privatethreads import check_private_threads_permission
from ..permissions.search import check_search_permission
from ..plugins import extensions
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
        return {
            "header": self.get_header_data(),
            "search_forms": self.get_search_forms(),
        }

    def get_header_data(self) -> dict:
        return {"template_name": self.header_template_name}

    def get_search_forms(self) -> list[SearchForm]:
        forms = [self.get_threads_search_form()]

        if private_threads_form := self.get_private_threads_search_form():
            forms.append(private_threads_form)

        if users_form := self.get_users_search_form():
            forms.append(users_form)

        return forms

    def get_threads_search_form(self) -> ThreadsSearchForm:
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


class ThreadsSearchView(View):
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

        if category_ids := filters.get("categories"):
            categories = [
                request.categories[category_id] for category_id in category_ids
            ]
        else:
            categories = list(request.categories.values())

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


class PrivateThreadsSearchView(ThreadsSearchView):
    pass


class UsersSearchView(View):
    pass


def debug_search(request: HttpRequest) -> HttpResponse:
    query = (request.GET.get("q") or "").strip()
    mode = (request.GET.get("mode") or "").strip()
    sorting = (request.GET.get("sorting") or "").strip()

    categories = []
    for category in request.categories.values():
        categories.append(category)

    valid_modes = ("threads", "posts", "thread_titles")
    if mode not in valid_modes:
        mode = valid_modes[0]

    valid_sortings = ("relevance", "newest")
    if sorting not in valid_sortings:
        sorting = valid_sortings[0]

    if query:
        if mode == "threads":
            results = posts_search.search_threads(
                query,
                request.user_permissions,
                categories=categories,
                order_by=SearchSort(sorting),
            )
        elif mode == "posts":
            results = posts_search.search_posts(
                query,
                request.user_permissions,
                categories=categories,
                order_by=SearchSort(sorting),
            )
        elif mode == "thread_titles":
            results = posts_search.search_thread_titles(
                query,
                request.user_permissions,
                categories=categories,
                order_by=SearchSort(sorting),
            )
    else:
        results = None

    return render(
        request,
        "misago/search/debug.html",
        {
            "query": query,
            "mode": mode,
            "sorting": sorting,
            "results": results,
        },
    )
