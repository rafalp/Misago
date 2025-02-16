import re
from math import ceil
from typing import Any, TYPE_CHECKING, Type

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404, HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import pgettext
from django.views import View

from ...categories.enums import CategoryChildrenComponent, CategoryTree
from ...categories.components import get_categories_data, get_subcategories_data
from ...categories.models import Category
from ...core.exceptions import OutdatedSlug
from ...metatags.metatag import MetaTag
from ...metatags.metatags import (
    get_default_metatags,
    get_forum_index_metatags,
)
from ...moderation.results import (
    ModerationBulkResult,
    ModerationResult,
    ModerationTemplateResult,
)
from ...moderation.threads import (
    CloseThreadsBulkModerationAction,
    MoveThreadsBulkModerationAction,
    OpenThreadsBulkModerationAction,
    ThreadsBulkModerationAction,
)
from ...pagination.cursor import (
    CursorPaginationResult,
    EmptyPageError,
    paginate_queryset,
)
from ...pagination.redirect import redirect_to_last_page
from ...permissions.categories import check_browse_category_permission
from ...permissions.checkutils import check_permissions
from ...permissions.enums import CategoryPermission
from ...permissions.privatethreads import (
    check_private_threads_permission,
    check_start_private_threads_permission,
    filter_private_threads_queryset,
)
from ...permissions.threads import (
    CategoryThreadsQuerysetFilter,
    ThreadsQuerysetFilter,
    check_start_thread_permission,
)
from ...readtracker.privatethreads import unread_private_threads_exist
from ...readtracker.threads import is_category_read
from ...readtracker.tracker import (
    annotate_categories_read_time,
    annotate_threads_read_time,
    get_unread_threads,
    mark_category_read,
)
from ...readtracker.models import ReadCategory, ReadThread
from ..enums import (
    ThreadsListsPolling,
    ThreadWeight,
)
from ..filters import (
    MyThreadsFilter,
    ThreadsFilter,
    ThreadsFilterChoice,
    UnapprovedThreadsFilter,
    UnreadThreadsFilter,
)
from ..hooks import (
    get_category_threads_page_context_data_hook,
    get_category_threads_page_filters_hook,
    get_category_threads_page_moderation_actions_hook,
    get_category_threads_page_queryset_hook,
    get_category_threads_page_subcategories_hook,
    get_category_threads_page_threads_hook,
    get_private_threads_page_context_data_hook,
    get_private_threads_page_filters_hook,
    get_private_threads_page_queryset_hook,
    get_private_threads_page_threads_hook,
    get_threads_page_context_data_hook,
    get_threads_page_filters_hook,
    get_threads_page_moderation_actions_hook,
    get_threads_page_queryset_hook,
    get_threads_page_subcategories_hook,
    get_threads_page_threads_hook,
)
from ..models import Thread

if TYPE_CHECKING:
    from ...users.models import User
else:
    User = get_user_model()

POLL_NEW_THREADS = "poll_new"
ANIMATE_NEW_THREADS = "animate_new"


class ListView(View):
    template_name: str
    template_name_htmx: str
    moderation_page_template_name: str
    moderation_modal_template_name: str
    threads_component_template_name = "misago/threads_list/index.html"
    new_threads_template_name = "misago/threads/poll_new.html"

    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        except EmptyPageError as exc:
            return redirect_to_last_page(request, exc)

    def get(self, request: HttpRequest, **kwargs):
        if (
            request.is_htmx
            and self.is_threads_polling_enabled(request)
            and POLL_NEW_THREADS in request.GET
        ):
            return self.poll_new_threads(request, kwargs)

        context = self.get_context_data(request, kwargs)

        if request.is_htmx:
            template_name = self.template_name_htmx
        else:
            template_name = self.template_name

        return render(request, template_name, context)

    def get_context_data(self, request: HttpRequest, kwargs: dict) -> dict:
        return {}

    def show_thread_flags(
        self,
        for_moderator: bool,
        thread: Thread,
        category: Category | None = None,
    ) -> bool:
        if (
            thread.weight == ThreadWeight.PINNED_GLOBALLY
            or thread.is_closed
            or thread.has_best_answer
            or thread.has_poll
        ):
            return True

        if thread.weight == ThreadWeight.PINNED_IN_CATEGORY and (
            (category and category.id == thread.category_id) or for_moderator
        ):
            return True

        if for_moderator and thread.has_unapproved_posts:
            return True

        return False

    def get_threads_users(self, request: HttpRequest, threads: list[Thread]) -> dict:
        user_ids: set[int] = set()
        for thread in threads:
            user_ids.add(thread.starter_id)
            user_ids.add(thread.last_poster_id)

        if not user_ids:
            return {}

        return {user.id: user for user in User.objects.filter(id__in=user_ids)}

    def get_threads_to_animate(
        self, request: HttpRequest, kwargs: dict, threads: list[Thread]
    ) -> dict[int, bool]:
        if "animate" in kwargs:
            return {thread.id: thread.id in kwargs["animate"] for thread in threads}

        if not request.is_htmx or ANIMATE_NEW_THREADS not in request.GET:
            return {}

        try:
            animate_threads = int(request.GET.get(ANIMATE_NEW_THREADS))
            if animate_threads < 0:
                raise Http404()
        except (ValueError, TypeError):
            raise Http404()

        return {thread.id: thread.last_post_id > animate_threads for thread in threads}

    def get_thread_urls(self, thread: Thread) -> dict[str, str]:
        kwargs = {"id": thread.id, "slug": thread.slug}

        return {
            "absolute_url": reverse("misago:thread", kwargs=kwargs),
            "last_post_url": reverse("misago:thread-last-post", kwargs=kwargs),
            "unapproved_post_url": reverse(
                "misago:thread-unapproved-post", kwargs=kwargs
            ),
            "unread_post_url": reverse("misago:thread-unread-post", kwargs=kwargs),
            "solution_post_url": reverse("misago:thread-solution-post", kwargs=kwargs),
        }

    def post_mark_as_read(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        current_url = request.get_full_path_info()
        if request.user.is_authenticated:
            if response := self.mark_as_read(request, kwargs):
                return response

        if request.is_htmx:
            return self.get(request, **kwargs)

        return redirect(current_url)

    def mark_as_read(self, request: HttpRequest, kwargs: dict) -> HttpResponse | None:
        raise NotImplementedError()

    @transaction.atomic
    def read_categories(self, user: "User", categories_ids: list[str]):
        if not categories_ids:
            return

        read_time = timezone.now()

        # Clear read tracker for categories
        ReadThread.objects.filter(user=user, category_id__in=categories_ids).delete()
        ReadCategory.objects.filter(user=user, category_id__in=categories_ids).delete()

        ReadCategory.objects.bulk_create(
            ReadCategory(user=user, read_time=read_time, category_id=category_id)
            for category_id in categories_ids
        )

    def post_moderation(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        try:
            current_url = request.get_full_path_info()
            result = self.moderate_threads(request, kwargs)

            if isinstance(result, ModerationTemplateResult):
                result.update_context(
                    {
                        "template_name": result.template_name,
                        "cancel_url": current_url,
                    }
                )

                if request.is_htmx:
                    template_name = self.moderation_modal_template_name
                else:
                    template_name = self.moderation_page_template_name

                return render(request, template_name, result.context)

            if request.is_htmx:
                if isinstance(result, ModerationBulkResult) and result.updated:
                    kwargs.update({"animate": result.updated})

                response = self.get(request, **kwargs)
                self.set_moderation_response_headers(request, response)
                return response

            return redirect(current_url)
        except ValidationError as e:
            messages.error(request, e.message)
            return self.get(request, **kwargs)

    def set_moderation_response_headers(
        self, request: HttpRequest, response: HttpResponse
    ):
        response.headers["hx-trigger"] = "misago:afterModeration"
        if request.POST.get("success-hx-target"):
            response.headers["hx-retarget"] = request.POST["success-hx-target"]
        if request.POST.get("success-hx-swap"):
            response.headers["hx-reswap"] = request.POST["success-hx-swap"]

    def moderate_threads(self, request: HttpRequest, kwargs) -> dict | None:
        raise NotImplementedError()

    def get_moderation_action(
        self, request: HttpRequest, threads: dict
    ) -> ThreadsBulkModerationAction | None:
        action_id = request.POST["moderation"]
        for action in threads["moderation_actions"]:
            if action.id == action_id:
                return action()

        raise ValidationError(
            pgettext("threads moderation error", "Invalid moderation action."),
        )

    def get_selected_threads(self, request: HttpRequest, threads: dict) -> list[Thread]:
        threads_ids = self.get_selected_threads_ids(request)

        selection: list[Thread] = []
        for thread_data in threads["items"]:
            thread = thread_data["thread"]
            if thread.id in threads_ids:
                if not thread_data["moderation"]:
                    raise ValidationError(
                        pgettext(
                            "threads moderation error",
                            'Can\'t moderate the "%(thread)s" thread.',
                        )
                        % {"thread": thread.title},
                    )

                selection.append(thread)

        if not selection:
            raise ValidationError(
                pgettext("threads moderation error", "No valid threads selected."),
            )

        return selection

    def get_selected_threads_ids(self, request: HttpRequest) -> set[int]:
        threads_ids: set[int] = set()
        for thread_id in request.POST.getlist("threads"):
            try:
                threads_ids.add(int(thread_id))
            except (TypeError, ValueError):
                pass
        return threads_ids

    def get_threads_latest_post_id(self, threads: list[Thread]) -> int:
        if threads:
            return max(t.last_post_id for t in threads)

        return 0

    def is_threads_polling_enabled(self, request: HttpRequest) -> bool:
        polling = request.settings.threads_lists_polling
        if polling == ThreadsListsPolling.DISABLED:
            return False

        if (
            polling == ThreadsListsPolling.ENABLED_FOR_USERS
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

    def allow_thread_moderation(self, request: HttpRequest, thread: Thread) -> bool:
        return request.user_permissions.is_category_moderator(thread.category_id)

    def get_metatags(self, request: HttpRequest, context: dict) -> dict:
        return get_default_metatags(request)

    def get_canonical_link(self, request: HttpRequest, context: dict) -> list:
        link = context["pagination_url"]
        if "cursor" in request.GET:
            link += "?cursor" + request.GET["cursor"]
        return link


class ThreadsListView(ListView):
    template_name = "misago/threads/index.html"
    template_name_htmx = "misago/threads/partial.html"
    mark_as_read_template_name = "misago/threads/mark_as_read_page.html"
    moderation_page_template_name = "misago/threads/moderation_page.html"
    moderation_modal_template_name = "misago/threads/moderation_modal.html"

    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        is_index: bool | None = None,
        **kwargs: Any,
    ) -> HttpResponse:
        if (
            not is_index
            and not kwargs.get("filter")
            and request.settings.index_view == "threads"
        ):
            return redirect(reverse("misago:index"))

        return super().dispatch(request, *args, is_index=is_index, **kwargs)

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if "mark_as_read" in request.POST:
            return self.post_mark_as_read(request, kwargs)

        if "moderation" in request.POST:
            return self.post_moderation(request, kwargs)

        return self.get(request, **kwargs)

    def mark_as_read(self, request: HttpRequest, kwargs: dict) -> HttpResponse | None:
        if not request.POST.get("confirm"):
            return render(request, self.mark_as_read_template_name)

        categories_ids = list(request.categories.categories)
        self.read_categories(request.user, categories_ids)
        messages.success(
            request, pgettext("mark threads as read", "Threads marked as read")
        )

    def moderate_threads(self, request: HttpRequest, kwargs) -> ModerationResult | None:
        threads = self.get_threads(request, kwargs)
        action = self.get_moderation_action(request, threads)
        selection = self.get_selected_threads(request, threads)

        result = action(request, selection)

        if isinstance(result, ModerationTemplateResult):
            result.update_context(
                {
                    "is_index": kwargs.get("is_index", False),
                    "moderation_action": action.get_context_data(),
                    "threads": threads,
                    "selection": selection,
                }
            )

        return result

    def get_context_data(self, request: HttpRequest, kwargs: dict):
        return get_threads_page_context_data_hook(
            self.get_context_data_action, request, kwargs
        )

    def get_context_data_action(self, request: HttpRequest, kwargs: dict):
        subcategories = self.get_subcategories(request)
        threads = self.get_threads(request, kwargs)

        context = {
            "template_name_htmx": self.template_name_htmx,
            "is_index": kwargs.get("is_index", False),
            "subcategories": subcategories,
            "threads": threads,
            "pagination_url": self.get_pagination_url(kwargs),
            "start_thread_modal": True,
            "start_thread_url": self.get_start_thread_url(request),
        }

        context["metatags"] = self.get_metatags(request, context)
        context["canonical_link"] = self.get_canonical_link(request, context)

        return context

    def get_subcategories(self, request: HttpRequest) -> dict | None:
        return get_threads_page_subcategories_hook(
            self.get_subcategories_action, request
        )

    def get_subcategories_action(self, request: HttpRequest) -> dict | None:
        component = request.settings.threads_list_categories_component

        if component == CategoryChildrenComponent.FULL:
            if request.is_htmx:
                return None

            return {
                "categories": get_categories_data(request),
                "template_name": "misago/threads/subcategories_full.html",
            }

        if component == CategoryChildrenComponent.DROPDOWN:
            return {
                "categories": [
                    c for c in request.categories.categories_list if c["level"] < 2
                ],
                "template_name": None,
            }

        return None

    def get_threads(self, request: HttpRequest, kwargs: dict):
        return get_threads_page_threads_hook(self.get_threads_action, request, kwargs)

    def get_threads_action(self, request: HttpRequest, kwargs: dict):
        filters_base_url = self.get_filters_base_url()
        active_filter, filters = self.get_threads_filters(
            request, filters_base_url, kwargs.get("filter")
        )

        permissions_filter = self.get_threads_permissions_queryset_filter(request)
        queryset = self.get_threads_queryset(request)

        if not active_filter or active_filter.url != "unread":
            queryset = annotate_threads_read_time(request.user, queryset)

        if active_filter:
            threads_queryset = active_filter.filter(queryset)
        else:
            threads_queryset = queryset

        paginator = self.get_threads_paginator(
            request, permissions_filter, threads_queryset
        )

        threads_list: list[Thread] = []
        if not paginator.has_previous:
            threads_list = self.get_pinned_threads(
                request, permissions_filter, queryset
            )

        threads_list += paginator.items

        users = self.get_threads_users(request, threads_list)
        animate = self.get_threads_to_animate(request, kwargs, threads_list)
        selected = self.get_selected_threads_ids(request)

        if active_filter and active_filter.url == "unread":
            unread = set(thread.id for thread in threads_list)
        else:
            unread = get_unread_threads(request, threads_list)

        items: list[dict] = []
        for thread in threads_list:
            categories = request.categories.get_thread_categories(thread.category_id)
            moderation = self.allow_thread_moderation(request, thread)

            thread_data = {
                "thread": thread,
                "unread": thread.id in unread,
                "starter": users.get(thread.starter_id),
                "last_poster": users.get(thread.last_poster_id),
                "pages": self.get_thread_pages_count(request, thread),
                "categories": categories,
                "moderation": moderation,
                "animate": animate.get(thread.id, False),
                "selected": thread.id in selected,
                "show_flags": self.show_thread_flags(moderation, thread),
            }

            thread_data.update(self.get_thread_urls(thread))
            items.append(thread_data)

        return {
            "template_name": self.threads_component_template_name,
            "latest_post": self.get_threads_latest_post_id(threads_list),
            "active_filter": active_filter,
            "filters": filters,
            "filters_clear_url": self.get_filters_clear_url(request),
            "moderation_actions": self.get_moderation_actions(request),
            "items": items,
            "paginator": paginator,
            "categories_component": (
                request.settings.threads_list_item_categories_component
            ),
            "enable_polling": self.is_threads_polling_enabled(request),
        }

    def get_filters_base_url(self) -> str:
        return reverse("misago:threads")

    def get_filters_clear_url(self, request: HttpRequest) -> str:
        if request.settings.index_view == "threads":
            return reverse("misago:index")

        return self.get_filters_base_url()

    def get_threads_filters(
        self, request: HttpRequest, base_url: str, filter: str | None
    ) -> tuple[ThreadsFilterChoice | None, list[ThreadsFilterChoice]]:
        active: ThreadsFilterChoice | None = None
        choices: list[ThreadsFilterChoice] = []

        filters = get_threads_page_filters_hook(
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

        filters = [
            UnreadThreadsFilter(request),
            MyThreadsFilter(request),
        ]

        if request.user_permissions.moderated_categories:
            filters.append(UnapprovedThreadsFilter(request))

        return filters

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

    def get_pagination_url(self, kwargs: dict) -> str:
        if kwargs["is_index"]:
            return reverse("misago:index")

        if kwargs.get("filter"):
            return reverse("misago:threads", kwargs={"filter": kwargs["filter"]})

        return reverse("misago:threads")

    def get_start_thread_url(self, request: HttpRequest) -> str | None:
        if request.user_permissions.categories[CategoryPermission.START]:
            return reverse("misago:start-thread")

    def get_moderation_actions(
        self, request: HttpRequest
    ) -> list[Type[ThreadsBulkModerationAction]]:
        return get_threads_page_moderation_actions_hook(
            self.get_moderation_actions_action, request
        )

    def get_moderation_actions_action(
        self, request: HttpRequest
    ) -> list[Type[ThreadsBulkModerationAction]]:
        actions: list = []
        if not request.user_permissions.moderated_categories:
            return actions

        actions += [
            OpenThreadsBulkModerationAction,
            CloseThreadsBulkModerationAction,
            MoveThreadsBulkModerationAction,
        ]

        return actions

    def poll_new_threads(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        filters_base_url = self.get_filters_base_url()
        active_filter, _ = self.get_threads_filters(
            request, filters_base_url, kwargs.get("filter")
        )

        cursor = self.get_poll_new_threads_cursor(request)
        new_threads = self.count_new_threads(request, active_filter, cursor)
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
        active_filter: ThreadsFilterChoice | None,
        after: int,
    ) -> int:
        permissions_filter = self.get_threads_permissions_queryset_filter(request)
        queryset = self.get_threads_queryset(request).filter(last_post_id__gt=after)

        if active_filter:
            threads_queryset = active_filter.filter(queryset)
        else:
            threads_queryset = queryset

        new_threads = permissions_filter.filter(threads_queryset).count()
        new_threads += permissions_filter.filter_pinned(queryset).count()

        return new_threads

    def get_metatags(self, request: HttpRequest, context: dict) -> dict:
        if context["is_index"]:
            return get_forum_index_metatags(request)

        return super().get_metatags(request, context)


class CategoryThreadsListView(ListView):
    template_name = "misago/category/index.html"
    template_name_htmx = "misago/category/partial.html"
    mark_as_read_template_name = "misago/category/mark_as_read_page.html"
    moderation_page_template_name = "misago/category/moderation_page.html"
    moderation_modal_template_name = "misago/threads/moderation_modal.html"

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if "mark_as_read" in request.POST:
            return self.post_mark_as_read(request, kwargs)

        if "moderation" in request.POST:
            return self.post_moderation(request, kwargs)

        return self.get(request, **kwargs)

    def mark_as_read(self, request: HttpRequest, kwargs: dict) -> HttpResponse | None:
        category = self.get_category(request, kwargs)

        if not request.POST.get("confirm"):
            return render(
                request,
                self.mark_as_read_template_name,
                {
                    "category": category,
                    "breadcrumbs": request.categories.get_category_path(
                        category.id, include_self=False
                    ),
                },
            )

        if category.list_children_threads:
            categories_ids = [
                c["id"]
                for c in request.categories.get_category_descendants(category.id)
            ]
        else:
            categories_ids = [category.id]

        self.read_categories(request.user, categories_ids)

        messages.success(
            request, pgettext("mark threads as read", "Category marked as read")
        )

    def moderate_threads(self, request: HttpRequest, kwargs) -> ModerationResult | None:
        category = self.get_category(request, kwargs)
        threads = self.get_threads(request, category, kwargs)
        action = self.get_moderation_action(request, threads)
        selection = self.get_selected_threads(request, threads)

        result = action(request, selection)

        if isinstance(result, ModerationTemplateResult):
            result.update_context(
                {
                    "category": category,
                    "moderation_action": action.get_context_data(),
                    "threads": threads,
                    "selection": selection,
                    "breadcrumbs": request.categories.get_category_path(
                        category.id, include_self=False
                    ),
                }
            )

        return result

    def get_context_data(self, request: HttpRequest, kwargs: dict):
        return get_category_threads_page_context_data_hook(
            self.get_context_data_action, request, kwargs
        )

    def get_context_data_action(self, request: HttpRequest, kwargs: dict):
        category = self.get_category(request, kwargs)

        if not category.is_vanilla or category.list_children_threads:
            threads = self.get_threads(request, category, kwargs)
        else:
            threads = None

        path = request.categories.get_category_path(category.id, include_self=False)

        context = {
            "template_name_htmx": self.template_name_htmx,
            "category": category,
            "subcategories": self.get_subcategories(request, category),
            "threads": threads,
            "breadcrumbs": path,
            "pagination_url": self.get_pagination_url(category, kwargs),
            "start_thread_url": self.get_start_thread_url(request, category),
        }

        self.raise_404_for_vanilla_category(category, context)

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
        context["canonical_link"] = self.get_canonical_link(request, context)

        return context

    def get_category(self, request: HttpRequest, kwargs: dict):
        try:
            queryset = annotate_categories_read_time(request.user, Category.objects)
            category = queryset.get(
                id=kwargs["id"],
                tree_id=CategoryTree.THREADS,
                level__gt=0,
            )
        except Category.DoesNotExist:
            raise Http404()

        check_browse_category_permission(
            request.user_permissions, category, can_delay=True
        )

        if category.slug != kwargs["slug"]:
            raise OutdatedSlug(category)

        return category

    def get_subcategories(
        self, request: HttpRequest, category: Category
    ) -> dict | None:
        if category.is_leaf_node():
            return None

        return get_category_threads_page_subcategories_hook(
            self.get_subcategories_action, request, category
        )

    def get_subcategories_action(
        self, request: HttpRequest, category: Category
    ) -> dict | None:
        component = category.children_categories_component

        if component == CategoryChildrenComponent.FULL:
            if request.is_htmx:
                return None

            categories = get_subcategories_data(request, category)
            if not categories:
                return None

            return {
                "categories": categories,
                "template_name": "misago/category/subcategories_full.html",
            }

        if component == CategoryChildrenComponent.DROPDOWN:
            categories = list(self.get_subcategories_dropdown_items(request, category))
            if not categories:
                return None

            return {
                "categories": categories,
                "template_name": None,
            }

        return None

    def get_subcategories_dropdown_items(
        self, request: HttpRequest, category: Category
    ):
        for c in request.categories.categories_list:
            if (
                c["lft"] > category.lft
                and c["rght"] < category.rght
                and c["level"] - category.level < 3
            ):
                category_data = c.copy()
                category_data["level"] -= category.level
                yield category_data

    def get_threads(self, request: HttpRequest, category: Category, kwargs: dict):
        return get_category_threads_page_threads_hook(
            self.get_threads_action, request, category, kwargs
        )

    def get_threads_action(
        self, request: HttpRequest, category: Category, kwargs: dict
    ):
        filters_base_url = self.get_filters_base_url(category)
        active_filter, filters = self.get_threads_filters(
            request, category, filters_base_url, kwargs.get("filter")
        )

        permissions_filter = self.get_threads_permissions_queryset_filter(
            request, category
        )
        queryset = self.get_threads_queryset(request)

        if not active_filter or active_filter.url != "unread":
            queryset = annotate_threads_read_time(request.user, queryset)

        if active_filter:
            threads_queryset = active_filter.filter(queryset)
        else:
            threads_queryset = queryset

        paginator = self.get_threads_paginator(
            request, permissions_filter, threads_queryset
        )

        threads_list: list[Thread] = []
        if not paginator.has_previous:
            threads_list = self.get_pinned_threads(
                request, permissions_filter, queryset
            )

        threads_list += paginator.items

        users = self.get_threads_users(request, threads_list)
        animate = self.get_threads_to_animate(request, kwargs, threads_list)
        selected = self.get_selected_threads_ids(request)

        if active_filter and active_filter.url == "unread":
            unread = set(thread.id for thread in threads_list)
        else:
            unread = get_unread_threads(request, threads_list)

        mark_read = bool(threads_list)

        items: list[dict] = []
        for thread in threads_list:
            categories = request.categories.get_thread_categories(
                thread.category_id, category.id
            )

            moderation = self.allow_thread_moderation(request, thread)

            if thread.category_id == category and thread.id in unread:
                mark_read = False

            thread_data = {
                "thread": thread,
                "unread": thread.id in unread,
                "starter": users.get(thread.starter_id),
                "last_poster": users.get(thread.last_poster_id),
                "pages": self.get_thread_pages_count(request, thread),
                "categories": categories,
                "moderation": moderation,
                "animate": animate.get(thread.id, False),
                "selected": thread.id in selected,
                "show_flags": self.show_thread_flags(moderation, thread),
            }

            thread_data.update(self.get_thread_urls(thread))
            items.append(thread_data)

        if (
            mark_read
            and self.is_category_unread(request.user, category)
            and is_category_read(request, category, category.read_time)
        ):
            mark_category_read(request.user, category)

        return {
            "template_name": self.threads_component_template_name,
            "latest_post": self.get_threads_latest_post_id(threads_list),
            "active_filter": active_filter,
            "filters": filters,
            "filters_clear_url": filters_base_url,
            "moderation_actions": self.get_moderation_actions(request, category),
            "items": items,
            "paginator": paginator,
            "categories_component": (
                request.settings.threads_list_item_categories_component
            ),
            "enable_polling": self.is_threads_polling_enabled(request),
        }

    def get_filters_base_url(self, category: Category) -> str:
        return category.get_absolute_url()

    def get_threads_filters(
        self,
        request: HttpRequest,
        category: Category,
        base_url: str,
        filter: str | None,
    ) -> tuple[ThreadsFilterChoice | None, list[ThreadsFilterChoice]]:
        active: ThreadsFilterChoice | None = None
        choices: list[ThreadsFilterChoice] = []

        filters = get_category_threads_page_filters_hook(
            self.get_threads_filters_action, request, category
        )

        for obj in filters:
            choice = obj.as_choice(base_url, obj.url == filter)
            if choice.active:
                active = choice
            choices.append(choice)

        if filter and not active:
            raise Http404()

        return active, choices

    def get_threads_filters_action(
        self, request: HttpRequest, category: Category
    ) -> list[ThreadsFilter]:
        if request.user.is_anonymous:
            return []

        filters = [
            UnreadThreadsFilter(request),
            MyThreadsFilter(request),
        ]

        if request.user_permissions.is_category_moderator(category.id):
            filters.append(UnapprovedThreadsFilter(request))

        return filters

    def get_threads_queryset(self, request: HttpRequest):
        return get_category_threads_page_queryset_hook(
            self.get_threads_queryset_action, request
        )

    def get_threads_queryset_action(self, request: HttpRequest):
        return Thread.objects

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

    def get_pagination_url(self, category: Category, kwargs: dict) -> str:
        return category.get_absolute_url()

    def get_start_thread_url(
        self, request: HttpRequest, category: Category
    ) -> str | None:
        try:
            check_start_thread_permission(request.user_permissions, category)
        except:
            return None
        else:
            return reverse(
                "misago:start-thread",
                kwargs={"id": category.id, "slug": category.slug},
            )

    def is_category_unread(self, user: "User", category: Category) -> bool:
        if user.is_anonymous:
            return False
        if not category.last_post_on:
            return False
        if not category.read_time:
            return True
        return category.last_post_on > category.read_time

    def get_moderation_actions(
        self, request: HttpRequest, category: Category
    ) -> list[Type[ThreadsBulkModerationAction]]:
        return get_category_threads_page_moderation_actions_hook(
            self.get_moderation_actions_action, request, category
        )

    def get_moderation_actions_action(
        self, request: HttpRequest, category: Category
    ) -> list[Type[ThreadsBulkModerationAction]]:
        actions: list = []
        if not self.show_moderation_actions_in_category(request, category):
            return actions

        actions += [
            OpenThreadsBulkModerationAction,
            CloseThreadsBulkModerationAction,
            MoveThreadsBulkModerationAction,
        ]

        return actions

    def show_moderation_actions_in_category(
        self, request: HttpRequest, category: Category
    ) -> bool:
        if request.user_permissions.is_global_moderator:
            return True

        categories_ids = set(
            c["id"] for c in request.categories.get_category_descendants(category.id)
        )

        return bool(
            request.user_permissions.moderated_categories.intersection(categories_ids)
        )

    def raise_404_for_vanilla_category(self, category: Category, context: dict):
        """Raise 404 for empty top-level vanilla category

        Ignore nested vanilla categories because using them is mistake on admin part.
        Ignore categories that display either subcategories or threads from subcategories.
        """
        if (
            category.is_vanilla
            and category.level == 1
            and not context["threads"]
            and not context["subcategories"]
        ):
            raise Http404()

    def poll_new_threads(self, request: HttpRequest, kwargs: dict) -> HttpResponse:
        category = self.get_category(request, kwargs)

        filters_base_url = self.get_filters_base_url(category)
        active_filter, _ = self.get_threads_filters(
            request, category, filters_base_url, kwargs.get("filter")
        )

        cursor = self.get_poll_new_threads_cursor(request)
        new_threads = self.count_new_threads(request, category, active_filter, cursor)
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
        self,
        request: HttpRequest,
        category: Category,
        active_filter: ThreadsFilterChoice | None,
        after: int,
    ) -> int:
        permissions_filter = self.get_threads_permissions_queryset_filter(
            request, category
        )
        queryset = self.get_threads_queryset(request).filter(last_post_id__gt=after)

        if active_filter:
            threads_queryset = active_filter.filter(queryset)
        else:
            threads_queryset = queryset

        new_threads = permissions_filter.filter(threads_queryset).count()
        new_threads += permissions_filter.filter_pinned(queryset).count()
        return new_threads

    def get_metatags(self, request: HttpRequest, context: dict) -> dict:
        metatags = super().get_metatags(request, context)

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


class PrivateThreadsListView(ListView):
    template_name = "misago/private_threads/index.html"
    template_name_htmx = "misago/private_threads/partial.html"
    mark_as_read_template_name = "misago/private_threads/mark_as_read_page.html"

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
        return get_private_threads_page_context_data_hook(
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
        queryset = annotate_categories_read_time(
            request.user, Category.objects.filter(tree_id=CategoryTree.PRIVATE_THREADS)
        )
        return queryset.first()

    def get_threads(self, request: HttpRequest, category: Category, kwargs: dict):
        return get_private_threads_page_threads_hook(
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
            queryset = annotate_threads_read_time(request.user, queryset)

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

        if mark_read and not unread_private_threads_exist(
            request, category, category.read_time
        ):
            mark_category_read(request.user, category)
            request.user.clear_unread_private_threads()

        return {
            "template_name": self.threads_component_template_name,
            "latest_post": self.get_threads_latest_post_id(threads_list),
            "active_filter": active_filter,
            "filters": filters,
            "filters_clear_url": filters_base_url,
            "items": items,
            "paginator": paginator,
            "enable_polling": self.is_threads_polling_enabled(request),
        }

    def get_filters_base_url(self) -> str:
        return reverse("misago:private-threads")

    def get_threads_filters(
        self, request: HttpRequest, base_url: str, filter: str | None
    ) -> tuple[ThreadsFilterChoice | None, list[ThreadsFilterChoice]]:
        active: ThreadsFilterChoice | None = None
        choices: list[ThreadsFilterChoice] = []

        filters = get_private_threads_page_filters_hook(
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
        )

    def get_thread_urls(self, thread: Thread) -> dict[str, str]:
        kwargs = {"id": thread.id, "slug": thread.slug}

        return {
            "absolute_url": reverse("misago:private-thread", kwargs=kwargs),
            "last_post_url": reverse("misago:private-thread-last-post", kwargs=kwargs),
            "unapproved_post_url": reverse(
                "misago:private-thread-unapproved-post", kwargs=kwargs
            ),
            "unread_post_url": reverse(
                "misago:private-thread-unread-post", kwargs=kwargs
            ),
        }

    def get_pagination_url(self, kwargs: dict) -> str:
        if kwargs.get("filter"):
            return reverse(
                "misago:private-threads",
                kwargs={"filter": kwargs["filter"]},
            )

        return reverse("misago:private-threads")

    def get_start_thread_url(self, request: HttpRequest) -> str | None:
        with check_permissions() as can_start_thread:
            check_start_private_threads_permission(request.user_permissions)

        if can_start_thread:
            return reverse("misago:start-private-thread")

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


threads = ThreadsListView.as_view()
category_threads = CategoryThreadsListView.as_view()
private_threads = PrivateThreadsListView.as_view()
