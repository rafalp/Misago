import re
from math import ceil
from typing import Any

from django.contrib.auth import get_user_model
from django.http import Http404, HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...metatags.metatag import MetaTag
from ...metatags.metatags import (
    get_default_metatags,
    get_forum_index_metatags,
)
from ...pagination.cursor import CursorPaginationResult, paginate_queryset
from ...permissions.categories import check_browse_category_permission
from ...permissions.private_threads import (
    check_private_threads_permission,
    filter_private_threads_queryset,
)
from ...permissions.threads import (
    CategoryThreadsQuerysetFilter,
    ThreadsQuerysetFilter,
)
from ..enums import PrivateThreadUrl, ThreadsListsPolling, ThreadUrl
from ..hooks import (
    get_category_threads_page_context_hook,
    get_category_threads_page_queryset_hook,
    get_category_threads_page_threads_hook,
    get_private_threads_page_context_hook,
    get_private_threads_page_queryset_hook,
    get_private_threads_page_threads_hook,
    get_threads_page_context_hook,
    get_threads_page_queryset_hook,
    get_threads_page_threads_hook,
)
from ..models import Thread

User = get_user_model()

POLL_NEW_THREADS = "poll_new"
ANIMATE_NEW_THREADS = "animate_new"


class ListView(View):
    template_name: str
    template_name_htmx: str
    threads_component_template_name = "misago/threads_list/index.html"
    new_threads_template_name = "misago/threads/poll_new.html"

    def get(self, request: HttpRequest, **kwargs):
        if (
            request.is_htmx
            and self.is_threads_polling_enabled(request)
            and POLL_NEW_THREADS in request.GET
        ):
            return self.poll_new_threads(request, kwargs)

        context = self.get_context(request, kwargs)

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context(self, request: HttpRequest, kwargs: dict):
        return {"request": request}

    def get_threads_users(self, request: HttpRequest, threads: list[Thread]) -> dict:
        user_ids: set[int] = set()
        for thread in threads:
            user_ids.add(thread.starter_id)
            user_ids.add(thread.last_poster_id)

        if not user_ids:
            return {}

        return {user.id: user for user in User.objects.filter(id__in=user_ids)}

    def get_threads_to_animate(
        self, request: HttpRequest, threads: list[Thread]
    ) -> dict[int, bool]:
        if not request.is_htmx or ANIMATE_NEW_THREADS not in request.GET:
            return {}

        try:
            animate_threads = int(request.GET.get(ANIMATE_NEW_THREADS))
            if animate_threads < 1:
                raise Http404()
        except (ValueError, TypeError):
            raise Http404()

        return {thread.id: thread.last_post_id > animate_threads for thread in threads}

    def get_threads_latest_post_id(self, threads: list[Thread]) -> int:
        if threads:
            return max(t.last_post_id for t in threads)

        return 0

    def is_threads_polling_enabled(self, request: HttpRequest) -> bool:
        if request.settings.threads_lists_polling == ThreadsListsPolling.DISABLED:
            return False

        if (
            request.settings.threads_lists_polling
            == ThreadsListsPolling.ENABLED_FOR_USERS
            and request.user.is_anonymous
        ):
            return False

        return True

    def poll_new_threads(self, request: HttpRequest, kwargs: dict):
        raise NotImplementedError()

    def get_poll_new_threads_cursor(self, request: HttpRequest):
        try:
            latest_post = int(request.GET.get(POLL_NEW_THREADS, 0))
            if latest_post < 0:
                raise Http404()
            return latest_post
        except (ValueError, TypeError):
            raise Http404()

    def get_thread_pages_count(self, request: HttpRequest, thread: Thread) -> int:
        posts = max(1, thread.replies + 1 - request.settings.posts_per_page_orphans)
        return ceil(posts / request.settings.posts_per_page)


class ThreadsListView(ListView):
    template_name = "misago/threads/index.html"
    template_name_htmx = "misago/threads/partial.html"

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
        return get_threads_page_context_hook(self.get_context_action, request, kwargs)

    def get_context_action(self, request: HttpRequest, kwargs: dict):
        threads = self.get_threads(request, kwargs)

        context = {
            "template_name_htmx": self.template_name_htmx,
            "request": request,
            "is_index": kwargs.get("is_index", False),
            "threads": threads,
            "pagination_url": self.get_pagination_url(kwargs),
        }

        context["metatags"] = self.get_metatags(request, context)

        return context

    def get_threads(self, request: HttpRequest, kwargs: dict):
        return get_threads_page_threads_hook(self.get_threads_action, request, kwargs)

    def get_threads_action(self, request: HttpRequest, kwargs: dict):
        permissions_filter = self.get_threads_permissions_queryset_filter(request)
        queryset = self.get_threads_queryset(request)
        paginator = self.get_threads_paginator(request, permissions_filter, queryset)

        threads_list: list[Thread] = []
        if not paginator.has_previous:
            threads_list = self.get_pinned_threads(
                request, permissions_filter, queryset
            )

        threads_list += paginator.items

        new_threads = {}
        users = self.get_threads_users(request, threads_list)
        animate = self.get_threads_to_animate(request, threads_list)

        items: list[dict] = []
        for thread in threads_list:
            categories = request.categories.get_thread_categories(thread.category_id)

            items.append(
                {
                    "thread": thread,
                    "is_new": new_threads.get(thread.id),
                    "starter": users.get(thread.starter_id),
                    "last_poster": users.get(thread.last_poster_id),
                    "pages": self.get_thread_pages_count(request, thread),
                    "categories": categories,
                    "animate": animate.get(thread.id, False),
                }
            )

        return {
            "template_name": self.threads_component_template_name,
            "latest_post": self.get_threads_latest_post_id(threads_list),
            "items": items,
            "paginator": paginator,
            "url_names": ThreadUrl.__members__,
            "categories_component": (
                request.settings.threads_list_item_categories_component
            ),
            "enable_polling": self.is_threads_polling_enabled(request),
        }

    def get_threads_queryset(self, request: HttpRequest):
        return get_threads_page_queryset_hook(self.get_threads_queryset_action, request)

    def get_threads_queryset_action(self, request: HttpRequest):
        return Thread.objects

    def get_threads_permissions_queryset_filter(
        self, request: HttpRequest
    ) -> ThreadsQuerysetFilter:
        return ThreadsQuerysetFilter(
            request.user_permissions, request.categories.categories_list
        )

    def get_threads_paginator(
        self,
        request: HttpRequest,
        permissions_filter: ThreadsQuerysetFilter,
        queryset,
    ) -> CursorPaginationResult:
        return paginate_queryset(
            request,
            permissions_filter.filter(queryset),
            request.settings.threads_per_page,
            order_by="-last_post_id",
            raise_404=True,
        )

    def get_pinned_threads(
        self,
        request: HttpRequest,
        permissions_filter: ThreadsQuerysetFilter,
        queryset,
    ) -> list[Thread]:
        return list(
            permissions_filter.filter_pinned(queryset).order_by(
                "-weight", "-last_post_id"
            )
        )

    def get_metatags(self, request: HttpRequest, context: dict) -> dict:
        if context["is_index"]:
            return get_forum_index_metatags(request)

        return {}

    def get_pagination_url(self, kwargs: dict) -> str:
        if kwargs["is_index"]:
            return reverse("misago:index")

        if kwargs.get("filter"):
            return reverse("misago:threads", kwargs={"filter": kwargs["filter"]})

        return reverse("misago:threads")

    def poll_new_threads(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        cursor = self.get_poll_new_threads_cursor(request)
        new_threads = self.count_new_threads(request, cursor)
        return render(
            request,
            self.new_threads_template_name,
            {
                "latest_post": cursor,
                "new_threads": new_threads,
                "pagination_url": self.get_pagination_url(kwargs),
            },
        )

    def count_new_threads(self, request: HttpRequest, after: int) -> int:
        permissions_filter = self.get_threads_permissions_queryset_filter(request)
        queryset = self.get_threads_queryset(request).filter(last_post_id__gt=after)

        new_threads = permissions_filter.filter_pinned(queryset).count()
        new_threads += permissions_filter.filter(queryset).count()
        return new_threads


class CategoryThreadsListView(ListView):
    template_name = "misago/category/index.html"
    template_name_htmx = "misago/category/partial.html"

    def get_context(self, request: HttpRequest, kwargs: dict):
        return get_category_threads_page_context_hook(
            self.get_context_action, request, kwargs
        )

    def get_context_action(self, request: HttpRequest, kwargs: dict):
        category = self.get_category(request, kwargs)

        if not category.is_vanilla or category.list_children_threads:
            threads = self.get_threads(request, category, kwargs)
        else:
            threads = None

        path = request.categories.get_category_path(category.id, include_self=False)

        context = {
            "template_name_htmx": self.template_name_htmx,
            "request": request,
            "category": category,
            "threads": threads,
            "breadcrumbs": path,
            "pagination_url": self.get_pagination_url(category, kwargs),
        }

        if kwargs.get("filter"):
            context["pagination_url"] = reverse(
                "misago:category",
                kwargs={
                    "id": category.id,
                    "slug": category.slug,
                    "filter": kwargs["filter"],
                },
            )
        else:
            context["pagination_url"] = category.get_absolute_url()

        context["metatags"] = self.get_metatags(request, context)

        return context

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
        return get_category_threads_page_threads_hook(
            self.get_threads_action, request, category, kwargs
        )

    def get_threads_action(
        self, request: HttpRequest, category: Category, kwargs: dict
    ):
        permissions_filter = self.get_threads_permissions_queryset_filter(
            request, category
        )
        queryset = self.get_threads_queryset(request)

        paginator = self.get_threads_paginator(request, permissions_filter, queryset)

        threads_list: list[Thread] = []
        if not paginator.has_previous:
            threads_list = self.get_pinned_threads(
                request, permissions_filter, queryset
            )

        threads_list += paginator.items

        new_threads = {}
        users = self.get_threads_users(request, threads_list)
        animate = self.get_threads_to_animate(request, threads_list)

        items: list[dict] = []
        for thread in threads_list:
            categories = request.categories.get_thread_categories(
                thread.category_id, category.id
            )

            items.append(
                {
                    "thread": thread,
                    "is_new": new_threads.get(thread.id),
                    "starter": users.get(thread.starter_id),
                    "last_poster": users.get(thread.last_poster_id),
                    "pages": self.get_thread_pages_count(request, thread),
                    "categories": categories,
                    "animate": animate.get(thread.id, False),
                }
            )

        return {
            "template_name": self.threads_component_template_name,
            "latest_post": self.get_threads_latest_post_id(threads_list),
            "items": items,
            "paginator": paginator,
            "url_names": ThreadUrl.__members__,
            "categories_component": (
                request.settings.threads_list_item_categories_component
            ),
            "enable_polling": self.is_threads_polling_enabled(request),
        }

    def get_threads_permissions_queryset_filter(
        self, request: HttpRequest, category: Category
    ) -> CategoryThreadsQuerysetFilter:
        categories = request.categories.get_category_descendants(category.id)

        return CategoryThreadsQuerysetFilter(
            request.user_permissions,
            request.categories.categories_list,
            current_category=categories[0],
            child_categories=categories[1:],
            include_children=category.list_children_threads,
        )

    def get_threads_queryset(self, request: HttpRequest):
        return get_category_threads_page_queryset_hook(
            self.get_threads_queryset_action, request
        )

    def get_threads_queryset_action(self, request: HttpRequest):
        return Thread.objects

    def get_threads_paginator(
        self,
        request: HttpRequest,
        permissions_filter: CategoryThreadsQuerysetFilter,
        queryset,
    ) -> CursorPaginationResult:
        return paginate_queryset(
            request,
            permissions_filter.filter(queryset),
            request.settings.threads_per_page,
            order_by="-last_post_id",
            raise_404=True,
        )

    def get_pinned_threads(
        self,
        request: HttpRequest,
        permissions_filter: CategoryThreadsQuerysetFilter,
        queryset,
    ) -> list[Thread]:
        return list(
            permissions_filter.filter_pinned(queryset).order_by(
                "-weight", "-last_post_id"
            )
        )

    def get_metatags(self, request: HttpRequest, context: dict) -> dict:
        metatags = get_default_metatags(request)

        category = context["category"]

        metatags.update(
            {
                "title": MetaTag(
                    property="og:title",
                    name="twitter:title",
                    content=category.name,
                ),
                "url": MetaTag(
                    property="og:url",
                    name="twitter:url",
                    content=category.get_absolute_url(),
                ),
            }
        )

        if category.description:
            metatags["description"] = MetaTag(
                property="og:description",
                name="twitter:description",
                content=re.sub(
                    "\n+",
                    " ",
                    category.description,
                ),
            )

        return metatags

    def get_pagination_url(self, category: Category, kwargs: dict) -> str:
        return category.get_absolute_url()

    def poll_new_threads(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        category = self.get_category(request, kwargs)
        cursor = self.get_poll_new_threads_cursor(request)
        new_threads = self.count_new_threads(request, category, cursor)
        return render(
            request,
            self.new_threads_template_name,
            {
                "latest_post": cursor,
                "new_threads": new_threads,
                "pagination_url": self.get_pagination_url(category, kwargs),
            },
        )

    def count_new_threads(
        self, request: HttpRequest, category: Category, after: int
    ) -> int:
        permissions_filter = self.get_threads_permissions_queryset_filter(
            request, category
        )
        queryset = self.get_threads_queryset(request).filter(last_post_id__gt=after)

        new_threads = permissions_filter.filter_pinned(queryset).count()
        new_threads += permissions_filter.filter(queryset).count()
        return new_threads


class PrivateThreadsListView(ListView):
    template_name = "misago/private_threads/index.html"
    template_name_htmx = "misago/private_threads/partial.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        check_private_threads_permission(request.user_permissions)

        return super().dispatch(request, *args, **kwargs)

    def get_context(self, request: HttpRequest, kwargs: dict):
        return get_private_threads_page_context_hook(
            self.get_context_action, request, kwargs
        )

    def get_context_action(self, request: HttpRequest, kwargs: dict):
        category = Category.objects.private_threads()

        context = {
            "template_name_htmx": self.template_name_htmx,
            "request": request,
            "threads": self.get_threads(request, category, kwargs),
            "pagination_url": self.get_pagination_url(kwargs),
        }

        context["metatags"] = self.get_metatags(request, {})

        return context

    def get_category(self, request: HttpRequest, kwargs: dict):
        return Category.objects.private_threads()

    def get_threads(self, request: HttpRequest, category: Category, kwargs: dict):
        return get_private_threads_page_threads_hook(
            self.get_threads_action, request, category, kwargs
        )

    def get_threads_action(
        self, request: HttpRequest, category: Category, kwargs: dict
    ):
        queryset = self.get_threads_queryset(request, category)
        paginator = self.get_threads_paginator(request, queryset)
        threads_list: list[Thread] = paginator.items

        new_threads = {}
        users = self.get_threads_users(request, threads_list)
        animate = self.get_threads_to_animate(request, threads_list)

        items: list[dict] = []
        for thread in threads_list:
            items.append(
                {
                    "thread": thread,
                    "is_new": new_threads.get(thread.id),
                    "starter": users.get(thread.starter_id),
                    "last_poster": users.get(thread.last_poster_id),
                    "pages": self.get_thread_pages_count(request, thread),
                    "categories": None,
                    "animate": animate.get(thread.id, False),
                }
            )

        return {
            "template_name": self.threads_component_template_name,
            "latest_post": self.get_threads_latest_post_id(threads_list),
            "items": items,
            "paginator": paginator,
            "url_names": PrivateThreadUrl.__members__,
            "enable_polling": self.is_threads_polling_enabled(request),
        }

    def get_threads_queryset(self, request: HttpRequest, category: Category):
        return get_private_threads_page_queryset_hook(
            self.get_threads_queryset_action, request, category
        )

    def get_threads_queryset_action(self, request: HttpRequest, category: Category):
        return Thread.objects.filter(category=category)

    def get_threads_paginator(self, request: HttpRequest, queryset):
        threads_queryset = filter_private_threads_queryset(
            request.user_permissions, queryset
        )

        return paginate_queryset(
            request,
            threads_queryset,
            request.settings.threads_per_page,
            order_by="-last_post_id",
            raise_404=True,
        )

    def get_metatags(self, request: HttpRequest, context: dict) -> dict:
        return get_default_metatags(request)

    def get_pagination_url(self, kwargs: dict) -> str:
        if kwargs.get("filter"):
            return reverse(
                "misago:private-threads",
                kwargs={"filter": kwargs["filter"]},
            )

        return reverse("misago:private-threads")

    def poll_new_threads(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        category = self.get_category(request, kwargs)
        cursor = self.get_poll_new_threads_cursor(request)
        new_threads = self.count_new_threads(request, category, cursor)
        return render(
            request,
            self.new_threads_template_name,
            {
                "latest_post": cursor,
                "new_threads": new_threads,
                "pagination_url": self.get_pagination_url(kwargs),
            },
        )

    def count_new_threads(
        self, request: HttpRequest, category: Category, after: int
    ) -> int:
        queryset = self.get_threads_queryset(request, category).filter(
            last_post_id__gt=after
        )
        return filter_private_threads_queryset(
            request.user_permissions, queryset
        ).count()


threads = ThreadsListView.as_view()
category_threads = CategoryThreadsListView.as_view()
private_threads = PrivateThreadsListView.as_view()
