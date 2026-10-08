from datetime import datetime, time, timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet, prefetch_related_objects
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import npgettext, pgettext
from django.views import View

from ..categories.models import Category
from ..categories.proxy import CategoryProxy
from ..permissions.checkutils import check_permissions
from ..permissions.privatethreads import check_private_threads_permission
from ..permissions.search import check_search_permission
from ..plugins import extensions
from ..threads.models import Post
from .categories import get_searchable_category_ids
from .enums import SearchMode, SearchSort
from .forms import (
    PrivateThreadsSearchForm,
    SearchForm,
    ThreadsSearchForm,
    UsersSearchForm,
)
from .logging import log_search
from .service import search
from .throttling import throttle_search
from .types import ThreadsSearchResult, ThreadsSearchResultItem


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
    results_template_name = "misago/search/threads/results.html"

    is_search_public: bool = True

    def get(self, request: HttpRequest) -> HttpResponse:
        self.check_permission()
        context = self.get_context_data()

        if request.is_htmx:
            template_name = context["template_name"]
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def check_permission(self):
        check_search_permission(self.request.user_permissions)

    def get_context_data(self) -> dict:
        form = self.get_search_form()
        search_throttled = self.get_search_throttling()

        if self.request.is_htmx and search_throttled:
            raise PermissionDenied(
                self.get_search_throttled_message(search_throttled),
            )

        if form.is_valid() and not search_throttled:
            self.log_search(form.cleaned_data["query"])
            search_results = self.get_search_results_data(form)
        else:
            search_results = None

        if self.request.is_htmx:
            # In HTMX return only search results component
            return search_results

        return {
            "page_title": form.name,
            "breadcrumbs": self.get_breadcrumbs(),
            "form": form,
            "search_throttled": search_throttled,
            "search_throttled_message": self.get_search_throttled_message(
                search_throttled
            ),
            "search_results": search_results,
        }

    def get_search_form(self) -> ThreadsSearchForm:
        form_class = extensions.get(ThreadsSearchForm)
        return form_class(self.request.GET, request=self.request)

    def get_search_throttling(self) -> int:
        if self.request.user_permissions.bypass_search_throttling:
            return 0

        return throttle_search(self.request)

    def get_search_throttled_message(self, throttled: int) -> str:
        return npgettext(
            "search results throttled message",
            "Wait %(seconds)s second before searching again.",
            "Wait %(seconds)s seconds before searching again.",
            throttled,
        ) % {"seconds": throttled}

    def log_search(self, search_query: str):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None

        log_search(user, self.request.user_ip, search_query, self.is_search_public)

    def get_search_results_data(self, form: ThreadsSearchForm) -> dict:
        from_throttle = (
            self.request.is_htmx and self.request.GET.get("throttled") == "true"
        )

        max_offset = self.get_max_search_offset()
        offset = self.get_search_offset(max_offset)

        results = self.search(form, offset)
        post_ids = [result.post_id for result in results]

        posts: dict[int, Post] = {}
        for post in self.get_posts_queryset(post_ids):
            posts[post.id] = post

        prefetch_related_objects(list(posts.values()), "poster")

        results_data = []
        for result in results:
            results_data.append(
                self.get_search_result_data(result, posts[result.post_id])
            )

        if results.has_more and offset < max_offset:
            more_url = self.get_more_url(form, offset + len(results))
        else:
            more_url = None

        return {
            "template_name": self.results_template_name,
            "title": self.get_search_results_title(results),
            "from_throttle": from_throttle,
            "results": results_data,
            "offset": offset,
            "has_more": bool(more_url),
            "more_url": more_url,
        }

    def get_max_search_offset(self) -> int:
        return max(settings.MISAGO_SEARCH.get("MAX_OFFSET", 0), 20)

    def get_search_offset(self, max_offset: int) -> int:
        try:
            if offset := self.request.GET.get("offset", 0):
                offset = int(offset)
            if offset < 0 or offset > max_offset:
                raise ValueError()

            return offset
        except (ValueError, TypeError):
            raise Http404()

    def search(self, form: ThreadsSearchForm, offset: int) -> ThreadsSearchResult:
        request = self.request

        filters = form.cleaned_data

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

        return search.search_threads(
            form.search_query,
            request.user_permissions,
            categories=categories,
            users=users,
            after=date_from,
            before=date_to,
            mode=SearchMode(mode),
            order_by=SearchSort(sort),
            offset=offset,
            limit=self.get_search_limit(),
        )

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

    def get_search_limit(self) -> tuple[int, int]:
        return max(settings.MISAGO_SEARCH.get("RESULT_SIZE", 0), 5)

    def get_posts_queryset(self, post_ids: list[int]) -> QuerySet[Post]:
        return Post.objects.filter(id__in=post_ids)

    def get_search_result_data(
        self, result: ThreadsSearchResultItem, post: Post
    ) -> dict:
        return {
            "id": post.id,
            "poster": post.poster,
            "poster_name": post.poster_name,
            "posted_at": post.posted_at,
            "categories": self.get_search_result_categories(post),
            "thread_title": result.thread_title,
            "post_content": result.post_content,
            "post_url": reverse("misago:post", kwargs={"post_id": post.id}),
        }

    def get_search_result_categories(self, post: Post) -> list[dict]:
        return self.request.categories.get_ancestors(
            post.category_id, include_self=True
        )

    def get_search_results_title(self, results: ThreadsSearchResult) -> str:
        results_num = len(results)

        if not results_num:
            return pgettext("search threads results title", "No threads found")

        if results.has_more:
            message = npgettext(
                "search threads results title",
                "Found %(results)s+ thread",
                "Found %(results)s+ threads",
                results_num,
            )
        else:
            message = npgettext(
                "search threads results title",
                "Found %(results)s thread",
                "Found %(results)s threads",
                results_num,
            )

        return message % {"results": results_num}

    def get_more_url(self, form: ThreadsSearchForm, offset: int | None = None) -> str:
        cleaned_data = form.cleaned_data

        data = [
            ("query", cleaned_data["query"]),
            ("mode", cleaned_data["mode"]),
            ("sort", cleaned_data["sort"]),
        ]

        if categories := cleaned_data.get("categories"):
            data += [("categories", category_id) for category_id in categories]

        if users := cleaned_data.get("users"):
            data += [("users", " ".join(user.slug for user in users))]

        if date_from := cleaned_data["date_from"]:
            data.append(("date_from", date_from))

        if date_to := cleaned_data["date_to"]:
            data.append(("date_to", date_to))

        if offset:
            data.append(("offset", offset))

        return f"{self.request.path}?{urlencode(data)}"


class PrivateThreadsSearchView(ThreadsSearchView):
    is_search_public: bool = False

    def get_results_data(self, form: ThreadsSearchForm) -> dict:
        request = self.request

        filters = form.cleaned_data

        mode = filters["mode"]
        sort = filters["sort"]

        users = filters.get("users")
        date_from = None
        date_to = None

        if date_from := filters.get("date_from"):
            date_from = timezone.make_aware(datetime.combine(date_from, time.min))
        if date_to := filters.get("date_to"):
            date_to = timezone.make_aware(
                datetime.combine(date_to + timedelta(days=1), time.min)
            )

        results = search.search_private_threads(
            form.search_query,
            request.user_permissions,
            users=users,
            after=date_from,
            before=date_to,
            mode=SearchMode(mode),
            order_by=SearchSort(sort),
        )

        return {
            "header": self.get_search_results_header(results),
            "results": results,
            "more_url": None,
        }

    def get_search_results_title(self, results: ThreadsSearchResult) -> str:
        results_num = len(results)

        if not results_num:
            return pgettext(
                "search private threads results title", "No private threads found"
            )

        if results.has_more:
            message = npgettext(
                "search private threads results title",
                "Found %(results)s+ private thread",
                "Found %(results)s+ private threads",
                results_num,
            )
        else:
            message = npgettext(
                "search private threads results title",
                "Found %(results)s private thread",
                "Found %(results)s private threads",
                results_num,
            )

        return message % {"results": results_num}


class UsersSearchView(BaseSearchView):
    pass
