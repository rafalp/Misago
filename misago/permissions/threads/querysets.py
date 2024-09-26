from typing import Iterable

from django.db.models import Q, QuerySet

from ...threads.enums import ThreadWeight
from ...threads.models import Thread
from ..enums import (
    CategoryPermission,
    CategoryQueryContext,
    CategoryThreadsQuery,
)
from ..hooks import (
    filter_thread_posts_queryset_hook,
    get_category_threads_category_query_hook,
    get_category_threads_pinned_category_query_hook,
    get_threads_category_query_hook,
    get_threads_pinned_category_query_hook,
    get_category_threads_query_hook,
    get_threads_query_orm_filter_hook,
)
from ..proxy import UserPermissionsProxy


class ThreadsQuerysetFilter:
    permissions: UserPermissionsProxy
    all_categories: list[dict]

    def __init__(
        self,
        permissions: UserPermissionsProxy,
        all_categories: list[dict],
    ) -> QuerySet:
        self.permissions = permissions
        self.all_categories = []

        for category in all_categories:
            if category["id"] in permissions.categories[CategoryPermission.BROWSE] or (
                category["id"] in permissions.categories[CategoryPermission.SEE]
                and category["delay_browse_check"]
            ):
                self.all_categories.append(category)

    def filter(self, queryset: QuerySet) -> QuerySet:
        categories_queries = self.get_categories_threads_queries()
        if not categories_queries:
            return queryset.none()

        filters: list[Q] = self.get_queryset_filters(categories_queries)
        return queryset.filter(_or_q(filters))

    def filter_pinned(self, queryset: QuerySet) -> QuerySet:
        categories_queries = self.get_categories_pinned_threads_queries()
        if not categories_queries:
            return queryset.none()

        filters: list[Q] = self.get_queryset_filters(categories_queries)
        return queryset.filter(_or_q(filters))

    def get_categories_threads_queries(self) -> dict[str, set[int]]:
        queries: dict[str, set[int]] = {}
        for category in self.all_categories:
            if query := get_threads_category_query(self.permissions, category):
                self.add_query_to_queries(queries, query, category)
        return queries

    def get_categories_pinned_threads_queries(self) -> dict[str, set[int]]:
        queries: dict[str, set[int]] = {}
        for category in self.all_categories:
            if query := get_threads_pinned_category_query(self.permissions, category):
                self.add_query_to_queries(queries, query, category)
        return queries

    def add_query_to_queries(
        self, queries: dict[str, set[int]], query: str | list[str], category: dict
    ) -> None:
        if isinstance(query, str):
            if query not in queries:
                queries[query] = set()
            queries[query].add(category["id"])

        else:
            for q in query:
                self.add_query_to_queries(queries, q, category)

    def get_queryset_filters(self, access_levels: dict[str, set[int]]) -> list[Q]:
        filters: list[Q] = []
        for query, categories_ids in access_levels.items():
            filter_ = get_threads_query_orm_filter(
                query, categories_ids, self.permissions.user.id
            )
            filters.append(filter_)

        return filters


class CategoryThreadsQuerysetFilter(ThreadsQuerysetFilter):
    current_category: dict
    child_categories: list[dict]
    other_categories: list[dict]
    include_children: bool

    def __init__(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        current_category: dict,
        child_categories: list[dict],
        include_children: bool,
    ) -> QuerySet:
        super().__init__(permissions, categories)

        self.current_category = current_category
        self.child_categories = []
        self.other_categories = []

        children_ids = set(c["id"] for c in child_categories)

        for category in self.all_categories:
            if category["id"] == current_category["id"]:
                continue
            elif category["id"] in children_ids:
                self.child_categories.append(category)
            else:
                self.other_categories.append(category)

        self.include_children = include_children

    def get_categories_threads_queries(self) -> dict[str, set[int]]:
        queries: dict[str, set[int]] = {}

        if query := get_category_threads_category_query(
            self.permissions, self.current_category, CategoryQueryContext.CURRENT
        ):
            self.add_query_to_queries(queries, query, self.current_category)

        if self.include_children:
            for category in self.child_categories:
                if query := get_category_threads_category_query(
                    self.permissions, category, CategoryQueryContext.CHILD
                ):
                    self.add_query_to_queries(queries, query, category)

        for category in self.other_categories:
            if query := get_category_threads_category_query(
                self.permissions, category, CategoryQueryContext.OTHER
            ):
                self.add_query_to_queries(queries, query, category)

        return queries

    def get_categories_pinned_threads_queries(self) -> dict[str, set[int]]:
        queries: dict[str, set[int]] = {}

        if query := get_category_threads_pinned_category_query(
            self.permissions, self.current_category, CategoryQueryContext.CURRENT
        ):
            self.add_query_to_queries(queries, query, self.current_category)

        for category in self.child_categories:
            if query := get_category_threads_pinned_category_query(
                self.permissions, category, CategoryQueryContext.CHILD
            ):
                self.add_query_to_queries(queries, query, category)

        for category in self.other_categories:
            if query := get_category_threads_pinned_category_query(
                self.permissions, category, CategoryQueryContext.OTHER
            ):
                self.add_query_to_queries(queries, query, category)

        return queries


def filter_category_threads_queryset(
    permissions: UserPermissionsProxy, category: dict, queryset: QuerySet
):
    if permissions.user.is_authenticated:
        user_id = permissions.user.id
    else:
        user_id = None

    query = get_category_threads_query(permissions, category)
    if isinstance(query, list):
        expression = _or_q(
            [get_threads_query_orm_filter(q, [category["id"]], user_id) for q in query]
        )
    else:
        expression = get_threads_query_orm_filter(query, [category["id"]], user_id)

    return queryset.filter(expression)


def get_category_threads_query(
    permissions: UserPermissionsProxy, category: dict
) -> str | list[str] | None:
    return get_category_threads_query_hook(
        _get_category_threads_query_action, permissions, category
    )


def _get_category_threads_query_action(
    permissions: UserPermissionsProxy, category: dict
) -> str | list[str] | None:
    if permissions.is_category_moderator(category["id"]):
        return CategoryThreadsQuery.ALL

    if category["show_started_only"]:
        if permissions.user.is_authenticated:
            return [
                CategoryThreadsQuery.USER_PINNED,
                CategoryThreadsQuery.USER_STARTED_NOT_PINNED,
            ]

        return CategoryThreadsQuery.ANON_PINNED

    if permissions.user.is_authenticated:
        return CategoryThreadsQuery.USER

    return CategoryThreadsQuery.ANON


def get_threads_category_query(
    permissions: UserPermissionsProxy, category: dict
) -> str | list[str] | None:
    return get_threads_category_query_hook(
        _get_threads_category_query_action, permissions, category
    )


def _get_threads_category_query_action(
    permissions: UserPermissionsProxy, category: dict
) -> str | list[str] | None:
    if permissions.is_category_moderator(category["id"]):
        return CategoryThreadsQuery.ALL_NOT_PINNED_GLOBALLY

    if category["show_started_only"]:
        if permissions.user.is_authenticated:
            return [
                CategoryThreadsQuery.USER_PINNED_IN_CATEGORY,
                CategoryThreadsQuery.USER_STARTED_NOT_PINNED,
            ]

        return CategoryThreadsQuery.ANON_PINNED_IN_CATEGORY

    if permissions.user.is_authenticated:
        return CategoryThreadsQuery.USER_NOT_PINNED_GLOBALLY

    return CategoryThreadsQuery.ANON_NOT_PINNED_GLOBALLY


def get_threads_pinned_category_query(
    permissions: UserPermissionsProxy, category: dict
) -> str | list[str] | None:
    return get_threads_pinned_category_query_hook(
        _get_threads_pinned_category_query_action, permissions, category
    )


def _get_threads_pinned_category_query_action(
    permissions: UserPermissionsProxy, category: dict
) -> str | list[str] | None:
    if permissions.is_category_moderator(category["id"]):
        return CategoryThreadsQuery.ALL_PINNED_GLOBALLY

    if permissions.user.is_authenticated:
        return CategoryThreadsQuery.USER_PINNED_GLOBALLY

    return CategoryThreadsQuery.ANON_PINNED_GLOBALLY


def get_category_threads_category_query(
    permissions: UserPermissionsProxy, category: dict, context: str
) -> str | list[str] | None:
    return get_category_threads_category_query_hook(
        _get_category_threads_category_query_action,
        permissions,
        category,
        context,
    )


def _get_category_threads_category_query_action(
    permissions: UserPermissionsProxy, category: dict, context: str
) -> str | list[str] | None:
    if context == CategoryQueryContext.OTHER:
        return None  # We don't display non-category items on category pages

    if permissions.is_category_moderator(category["id"]):
        if context == CategoryQueryContext.CURRENT:
            return CategoryThreadsQuery.ALL_NOT_PINNED

        return CategoryThreadsQuery.ALL_NOT_PINNED_GLOBALLY

    if category["show_started_only"]:
        if context == CategoryQueryContext.CURRENT:
            if permissions.user.is_authenticated:
                return CategoryThreadsQuery.USER_STARTED_NOT_PINNED

            return None

        if permissions.user.is_authenticated:
            return [
                CategoryThreadsQuery.USER_PINNED_IN_CATEGORY,
                CategoryThreadsQuery.USER_STARTED_NOT_PINNED,
            ]

        return CategoryThreadsQuery.ANON_PINNED_IN_CATEGORY

    if context == CategoryQueryContext.CURRENT:
        if permissions.user.is_authenticated:
            return CategoryThreadsQuery.USER_NOT_PINNED

        return CategoryThreadsQuery.ANON_NOT_PINNED

    if permissions.user.is_authenticated:
        return CategoryThreadsQuery.USER_NOT_PINNED_GLOBALLY

    return CategoryThreadsQuery.ANON_NOT_PINNED_GLOBALLY


def get_category_threads_pinned_category_query(
    permissions: UserPermissionsProxy, category: dict, context: str
) -> str | list[str] | None:
    return get_category_threads_pinned_category_query_hook(
        _get_category_threads_pinned_category_query_action,
        permissions,
        category,
        context,
    )


def _get_category_threads_pinned_category_query_action(
    permissions: UserPermissionsProxy, category: dict, context: str
) -> str | list[str] | None:
    if permissions.is_category_moderator(category["id"]):
        if context == CategoryQueryContext.CURRENT:
            return CategoryThreadsQuery.ALL_PINNED

        return CategoryThreadsQuery.ALL_PINNED_GLOBALLY

    if permissions.user.is_authenticated:
        if context == CategoryQueryContext.CURRENT:
            return CategoryThreadsQuery.USER_PINNED

        return CategoryThreadsQuery.USER_PINNED_GLOBALLY

    if context == CategoryQueryContext.CURRENT:
        return CategoryThreadsQuery.ANON_PINNED

    return CategoryThreadsQuery.ANON_PINNED_GLOBALLY


def _or_q(q: Iterable[Q]):
    fin = None
    for cond in q:
        if cond:
            if fin is not None:
                fin |= cond
            else:
                fin = cond
    return fin


def get_threads_query_orm_filter(
    query: CategoryThreadsQuery | str,
    categories: set[int],
    user_id: int | None,
) -> Q:
    q = get_threads_query_orm_filter_hook(
        _get_threads_query_orm_filter_action, query, categories, user_id
    )

    if q is None:
        raise ValueError(f"Could not find a filter for the '{query}' query.")

    return q


def _get_threads_query_orm_filter_action(
    query: CategoryThreadsQuery | str,
    categories: set[int],
    user_id: int | None,
) -> Q | None:
    if query == CategoryThreadsQuery.ALL:
        return Q(category_id__in=categories)

    if query == CategoryThreadsQuery.ALL_PINNED:
        return Q(
            category_id__in=categories,
            weight__gt=ThreadWeight.NOT_PINNED,
        )

    if query == CategoryThreadsQuery.ALL_PINNED_GLOBALLY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_GLOBALLY,
        )

    if query == CategoryThreadsQuery.ALL_PINNED_IN_CATEGORY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_GLOBALLY,
        )

    if query == CategoryThreadsQuery.ALL_NOT_PINNED:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.NOT_PINNED,
        )

    if query == CategoryThreadsQuery.ALL_NOT_PINNED_GLOBALLY:
        return Q(
            category_id__in=categories,
            weight__lt=ThreadWeight.PINNED_GLOBALLY,
        )

    if query == CategoryThreadsQuery.ANON:
        return Q(
            category_id__in=categories,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_PINNED:
        return Q(
            category_id__in=categories,
            weight__gt=ThreadWeight.NOT_PINNED,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_PINNED_GLOBALLY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_GLOBALLY,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_PINNED_IN_CATEGORY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_IN_CATEGORY,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_NOT_PINNED:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.NOT_PINNED,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_NOT_PINNED_GLOBALLY:
        return Q(
            category_id__in=categories,
            weight__lt=ThreadWeight.PINNED_GLOBALLY,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.USER:
        return Q(
            category_id__in=categories,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_PINNED:
        return Q(
            category_id__in=categories,
            weight__gt=ThreadWeight.NOT_PINNED,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_PINNED_GLOBALLY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_GLOBALLY,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_PINNED_IN_CATEGORY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_IN_CATEGORY,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_NOT_PINNED:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.NOT_PINNED,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_NOT_PINNED_GLOBALLY:
        return Q(
            category_id__in=categories,
            weight__lt=ThreadWeight.PINNED_GLOBALLY,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_STARTED_PINNED:
        return Q(
            category_id__in=categories,
            weight__gt=ThreadWeight.NOT_PINNED,
            is_hidden=False,
            starter_id=user_id,
        )

    if query == CategoryThreadsQuery.USER_STARTED_PINNED_GLOBALLY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_GLOBALLY,
            is_hidden=False,
            starter_id=user_id,
        )

    if query == CategoryThreadsQuery.USER_STARTED_PINNED_IN_CATEGORY:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.PINNED_IN_CATEGORY,
            is_hidden=False,
            starter_id=user_id,
        )

    if query == CategoryThreadsQuery.USER_STARTED_NOT_PINNED:
        return Q(
            category_id__in=categories,
            weight=ThreadWeight.NOT_PINNED,
            is_hidden=False,
            starter_id=user_id,
        )

    return None


def filter_thread_posts_queryset(
    permissions: UserPermissionsProxy,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    return filter_thread_posts_queryset_hook(
        _filter_thread_posts_queryset_action, permissions, thread, queryset
    )


def _filter_thread_posts_queryset_action(
    permissions: UserPermissionsProxy,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    if permissions.is_category_moderator(thread.category_id):
        return queryset

    if permissions.user.is_authenticated:
        return queryset.filter(
            Q(is_unapproved=False) | Q(poster_id=permissions.user.id)
        )

    return queryset.filter(is_unapproved=False)
