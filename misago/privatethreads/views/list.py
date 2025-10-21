from typing import Any

from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import pgettext

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...pagination.cursor import paginate_queryset
from ...permissions.checkutils import check_permissions
from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_start_private_threads_permission,
    filter_private_threads_queryset,
)
from ...readtracker.privatethreads import unread_private_threads_exist
from ...readtracker.tracker import (
    categories_select_related_user_readcategory,
    get_category_read_time,
    get_unread_threads,
    threads_annotate_user_readcategory_time,
    threads_select_related_user_readthread,
    mark_category_read,
)
from ...threads.filters import (
    MyThreadsFilter,
    ThreadsFilter,
    ThreadsFilterChoice,
    UnreadThreadsFilter,
)
from ...threads.models import Thread
from ...threads.views.list import ListView
from ..hooks import (
    get_private_thread_list_context_data_hook,
    get_private_thread_list_filters_hook,
    get_private_thread_list_queryset_hook,
    get_private_thread_list_threads_hook,
)


class PrivateThreadListView(ListView):
    template_name = "misago/private_thread_list/index.html"
    template_name_htmx = "misago/private_thread_list/partial.html"
    mark_as_read_template_name = "misago/private_thread_list/mark_as_read_page.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        check_private_threads_permission(request.user_permissions)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if "mark_as_read" in request.POST:
            return self.post_mark_as_read(request, kwargs)

        return self.get(request, **kwargs)

    def mark_as_read(self, request: HttpRequest, kwargs: dict) -> HttpResponse | None:
        if not request.POST.get("confirm"):
            return render(
                request,
                self.mark_as_read_template_name,
                {},
            )

        category = self.get_category(request, kwargs)
        self.read_categories(request.user, [category.id])

        request.user.clear_unread_private_threads()

        messages.success(
            request, pgettext("mark threads as read", "Private threads marked as read")
        )

    def get_context_data(self, request: HttpRequest, kwargs: dict):
        return get_private_thread_list_context_data_hook(
            self.get_context_data_action, request, kwargs
        )

    def get_context_data_action(self, request: HttpRequest, kwargs: dict):
        category = self.get_category(request, kwargs)

        context = {
            "template_name_htmx": self.template_name_htmx,
            "threads": self.get_threads(request, category, kwargs),
            "pagination_url": self.get_pagination_url(kwargs),
            "start_thread_url": self.get_start_thread_url(request),
        }

        context["metatags"] = self.get_metatags(request, {})

        return context

    def get_category(self, request: HttpRequest, kwargs: dict):
        queryset = categories_select_related_user_readcategory(
            Category.objects.filter(tree_id=CategoryTree.PRIVATE_THREADS), request.user
        )
        return queryset.first()

    def get_threads(self, request: HttpRequest, category: Category, kwargs: dict):
        return get_private_thread_list_threads_hook(
            self.get_threads_action, request, category, kwargs
        )

    def get_threads_action(
        self, request: HttpRequest, category: Category, kwargs: dict
    ):
        filters_base_url = self.get_filters_base_url()
        active_filter, filters = self.get_threads_filters(
            request, filters_base_url, kwargs.get("filter")
        )

        queryset = self.get_threads_queryset(request, category)

        if not active_filter or active_filter.url != "unread":
            queryset = threads_select_related_user_readthread(queryset, request.user)
            queryset = threads_annotate_user_readcategory_time(queryset, request.user)

        if active_filter:
            queryset = active_filter.filter(queryset)

        paginator = self.get_threads_paginator(request, queryset)
        threads_list: list[Thread] = paginator.items

        users = self.get_threads_users(request, threads_list)
        animate = self.get_threads_to_animate(request, kwargs, threads_list)

        if active_filter and active_filter.url == "unread":
            unread = set(thread.id for thread in threads_list)
        else:
            unread = get_unread_threads(request, threads_list)

        mark_read = bool(threads_list)

        moderator = request.user_permissions.is_private_threads_moderator

        items: list[dict] = []
        for thread in threads_list:
            if thread.category_id == category and thread.id in unread:
                mark_read = False

            thread_data = {
                "thread": thread,
                "unread": thread.id in unread,
                "starter": users.get(thread.starter_id),
                "last_poster": users.get(thread.last_poster_id),
                "pages": self.get_thread_pages_count(request, thread),
                "categories": None,
                "animate": animate.get(thread.id, False),
                "show_flags": self.show_thread_flags(moderator, thread),
            }

            thread_data.update(self.get_thread_urls(thread))
            items.append(thread_data)

        category_read_time = get_category_read_time(category)
        if mark_read and not unread_private_threads_exist(
            request, category, category_read_time
        ):
            mark_category_read(request.user, category)
            request.user.clear_unread_private_threads()

        return {
            "template_name": self.list_items_component_template_name,
            "latest_post": self.get_threads_latest_post_id(threads_list),
            "active_filter": active_filter,
            "filters": filters,
            "filters_clear_url": filters_base_url,
            "items": items,
            "paginator": paginator,
            "enable_polling": self.is_threads_polling_enabled(request),
        }

    def get_filters_base_url(self) -> str:
        return reverse("misago:private-thread-list")

    def get_threads_filters(
        self, request: HttpRequest, base_url: str, filter: str | None
    ) -> tuple[ThreadsFilterChoice | None, list[ThreadsFilterChoice]]:
        active: ThreadsFilterChoice | None = None
        choices: list[ThreadsFilterChoice] = []

        filters = get_private_thread_list_filters_hook(
            self.get_threads_filters_action, request
        )

        for obj in filters:
            choice = obj.as_choice(base_url, obj.url == filter)
            if choice.active:
                active = choice
            choices.append(choice)

        if filter and not active:
            raise Http404()

        return active, choices

    def get_threads_filters_action(self, request: HttpRequest) -> list[ThreadsFilter]:
        if request.user.is_anonymous:
            return []

        return [
            UnreadThreadsFilter(request),
            MyThreadsFilter(request),
        ]

    def get_threads_queryset(self, request: HttpRequest, category: Category):
        return get_private_thread_list_queryset_hook(
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
        )

    def get_thread_urls(self, thread: Thread) -> dict[str, str]:
        kwargs = {"thread_id": thread.id, "slug": thread.slug}

        return {
            "absolute_url": reverse("misago:private-thread", kwargs=kwargs),
            "last_post_url": reverse("misago:private-thread-post-last", kwargs=kwargs),
            "unread_post_url": reverse(
                "misago:private-thread-post-unread", kwargs=kwargs
            ),
        }

    def get_pagination_url(self, kwargs: dict) -> str:
        if kwargs.get("filter"):
            return reverse(
                "misago:private-thread-list",
                kwargs={"filter": kwargs["filter"]},
            )

        return reverse("misago:private-thread-list")

    def get_start_thread_url(self, request: HttpRequest) -> str | None:
        with check_permissions() as can_start_thread:
            check_start_private_threads_permission(request.user_permissions)

        if can_start_thread:
            return reverse("misago:private-thread-start")

        return None

    def poll_new_threads(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        category = self.get_category(request, kwargs)

        filters_base_url = self.get_filters_base_url()
        active_filter, _ = self.get_threads_filters(
            request, filters_base_url, kwargs.get("filter")
        )

        cursor = self.get_poll_new_threads_cursor(request)
        new_threads = self.count_new_threads(request, category, active_filter, cursor)

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
        self,
        request: HttpRequest,
        category: Category,
        active_filter: ThreadsFilterChoice | None,
        after: int,
    ) -> int:
        queryset = self.get_threads_queryset(request, category).filter(
            last_post_id__gt=after
        )
        queryset = filter_private_threads_queryset(request.user_permissions, queryset)

        if active_filter:
            queryset = active_filter.filter(queryset)

        return queryset.count()
