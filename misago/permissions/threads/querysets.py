from typing import Iterable, Iterator, TypedDict

from django.db.models import Q, QuerySet

from ...threads.enums import ThreadPinned
from ...threads.models import Thread
from ..enums import (
    CategoryPermission,
    CategoryQueryContext,
    CategoryThreadsQuery,
)
from ..hooks import (
    filter_thread_posts_queryset_hook,
    filter_thread_updates_queryset_hook,
    get_category_threads_category_query_hook,
    get_category_threads_pinned_category_query_hook,
    get_category_threads_query_hook,
    get_threads_category_query_hook,
    get_threads_pinned_category_query_hook,
    get_threads_query_orm_filter_hook,
)
from ..proxy import UserPermissionsProxy


class CategoryDict(TypedDict):
    id: int
    delay_browse_check: bool


class CategoryQueries:
    _queries: dict[str, set[int]]

    def __init__(self):
        self._queries = {}

    def __len__(self) -> int:
        return len(self._queries)

    def add(
        self,
        query: str | list[str],
        category: CategoryDict,
    ) -> None:
        queries = self._queries

        if isinstance(query, str):
            if query not in queries:
                queries[query] = set()
            queries[query].add(category["id"])

        else:
            for q in query:
                self.add(q, category)

    def items(self) -> Iterator[tuple[str, set[int]]]:
        yield from self._queries.items()


class ThreadsQuerysetFilter:
    permissions: UserPermissionsProxy
    all_categories: list[CategoryDict]

    def __init__(
        self,
        permissions: UserPermissionsProxy,
        all_categories: list[CategoryDict],
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

    def get_categories_threads_queries(self) -> CategoryQueries:
        queries = CategoryQueries()
        for category in self.all_categories:
            if query := get_threads_category_query(self.permissions, category):
                queries.add(query, category)
        return queries

    def get_categories_pinned_threads_queries(self) -> CategoryQueries:
        queries = CategoryQueries()
        for category in self.all_categories:
            if query := get_threads_pinned_category_query(self.permissions, category):
                queries.add(query, category)
        return queries

    def get_queryset_filters(self, queries: CategoryQueries) -> list[Q]:
        filters: list[Q] = []
        for query, categories_ids in queries.items():
            filter_ = get_threads_query_orm_filter(
                query, categories_ids, self.permissions.user.id
            )
            filters.append(filter_)

        return filters


class CategoryThreadsQuerysetFilter(ThreadsQuerysetFilter):
    current_category: CategoryDict
    child_categories: list[CategoryDict]
    other_categories: list[CategoryDict]
    include_children: bool

    def __init__(
        self,
        permissions: UserPermissionsProxy,
        categories: list[CategoryDict],
        current_category: CategoryDict,
        child_categories: list[CategoryDict],
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

    def get_categories_threads_queries(self) -> CategoryQueries:
        queries = CategoryQueries()

        if query := get_category_threads_category_query(
            self.permissions, self.current_category, CategoryQueryContext.CURRENT
        ):
            queries.add(query, self.current_category)

        if self.include_children:
            for category in self.child_categories:
                if query := get_category_threads_category_query(
                    self.permissions, category, CategoryQueryContext.CHILD
                ):
                    queries.add(query, category)

        for category in self.other_categories:
            if query := get_category_threads_category_query(
                self.permissions, category, CategoryQueryContext.OTHER
            ):
                queries.add(query, category)

        return queries

    def get_categories_pinned_threads_queries(self) -> CategoryQueries:
        queries = CategoryQueries()

        if query := get_category_threads_pinned_category_query(
            self.permissions, self.current_category, CategoryQueryContext.CURRENT
        ):
            queries.add(query, self.current_category)

        for category in self.child_categories:
            if query := get_category_threads_pinned_category_query(
                self.permissions, category, CategoryQueryContext.CHILD
            ):
                queries.add(query, category)

        for category in self.other_categories:
            if query := get_category_threads_pinned_category_query(
                self.permissions, category, CategoryQueryContext.OTHER
            ):
                queries.add(query, category)

        return queries


def filter_threads_queryset(
    permissions: UserPermissionsProxy,
    categories: list[CategoryDict],
    queryset: QuerySet,
):
    valid_categories = []
    for category in categories:
        if category["id"] in permissions.categories[CategoryPermission.BROWSE] or (
            category["id"] in permissions.categories[CategoryPermission.SEE]
            and category["delay_browse_check"]
        ):
            valid_categories.append(category)

    queries = CategoryQueries()
    for category in valid_categories:
        if query := get_category_threads_query(permissions, category):
            queries.add(query, category)

    if not queries:
        return queryset.none()

    user_id = permissions.user.id
    expression = _or_q(
        [
            get_threads_query_orm_filter(query, category_ids, user_id)
            for query, category_ids in queries.items()
        ]
    )

    return queryset.filter(expression)


def filter_category_threads_queryset(
    permissions: UserPermissionsProxy, category: CategoryDict, queryset: QuerySet
):
    user_id = permissions.user.id
    query = get_category_threads_query(permissions, category)
    category_id = category["id"]

    if not query:
        return queryset.none()

    if isinstance(query, list):
        expression = _or_q(
            [get_threads_query_orm_filter(q, [category_id], user_id) for q in query]
        )
    else:
        expression = get_threads_query_orm_filter(query, [category_id], user_id)

    return queryset.filter(expression)


def get_category_threads_query(
    permissions: UserPermissionsProxy, category: CategoryDict
) -> str | list[str] | None:
    return get_category_threads_query_hook(
        _get_category_threads_query_action, permissions, category
    )


def _get_category_threads_query_action(
    permissions: UserPermissionsProxy, category: CategoryDict
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
    permissions: UserPermissionsProxy, category: CategoryDict
) -> str | list[str] | None:
    return get_threads_category_query_hook(
        _get_threads_category_query_action, permissions, category
    )


def _get_threads_category_query_action(
    permissions: UserPermissionsProxy, category: CategoryDict
) -> str | list[str] | None:
    if permissions.is_category_moderator(category["id"]):
        return CategoryThreadsQuery.ALL_NOT_PINNED_EVERYWHERE

    if category["show_started_only"]:
        if permissions.user.is_authenticated:
            return [
                CategoryThreadsQuery.USER_PINNED_CATEGORY,
                CategoryThreadsQuery.USER_STARTED_NOT_PINNED,
            ]

        return CategoryThreadsQuery.ANON_PINNED_CATEGORY

    if permissions.user.is_authenticated:
        return CategoryThreadsQuery.USER_NOT_PINNED_EVERYWHERE

    return CategoryThreadsQuery.ANON_NOT_PINNED_EVERYWHERE


def get_threads_pinned_category_query(
    permissions: UserPermissionsProxy, category: CategoryDict
) -> str | list[str] | None:
    return get_threads_pinned_category_query_hook(
        _get_threads_pinned_category_query_action, permissions, category
    )


def _get_threads_pinned_category_query_action(
    permissions: UserPermissionsProxy, category: CategoryDict
) -> str | list[str] | None:
    if permissions.is_category_moderator(category["id"]):
        return CategoryThreadsQuery.ALL_PINNED_EVERYWHERE

    if permissions.user.is_authenticated:
        return CategoryThreadsQuery.USER_PINNED_EVERYWHERE

    return CategoryThreadsQuery.ANON_PINNED_EVERYWHERE


def get_category_threads_category_query(
    permissions: UserPermissionsProxy, category: CategoryDict, context: str
) -> str | list[str] | None:
    return get_category_threads_category_query_hook(
        _get_category_threads_category_query_action,
        permissions,
        category,
        context,
    )


def _get_category_threads_category_query_action(
    permissions: UserPermissionsProxy, category: CategoryDict, context: str
) -> str | list[str] | None:
    if context == CategoryQueryContext.OTHER:
        return None  # We don't display non-category items on category pages

    if permissions.is_category_moderator(category["id"]):
        if context == CategoryQueryContext.CURRENT:
            return CategoryThreadsQuery.ALL_NOT_PINNED

        return CategoryThreadsQuery.ALL_NOT_PINNED_EVERYWHERE

    if category["show_started_only"]:
        if context == CategoryQueryContext.CURRENT:
            if permissions.user.is_authenticated:
                return CategoryThreadsQuery.USER_STARTED_NOT_PINNED

            return None

        if permissions.user.is_authenticated:
            return [
                CategoryThreadsQuery.USER_PINNED_CATEGORY,
                CategoryThreadsQuery.USER_STARTED_NOT_PINNED,
            ]

        return CategoryThreadsQuery.ANON_PINNED_CATEGORY

    if context == CategoryQueryContext.CURRENT:
        if permissions.user.is_authenticated:
            return CategoryThreadsQuery.USER_NOT_PINNED

        return CategoryThreadsQuery.ANON_NOT_PINNED

    if permissions.user.is_authenticated:
        return CategoryThreadsQuery.USER_NOT_PINNED_EVERYWHERE

    return CategoryThreadsQuery.ANON_NOT_PINNED_EVERYWHERE


def get_category_threads_pinned_category_query(
    permissions: UserPermissionsProxy, category: CategoryDict, context: str
) -> str | list[str] | None:
    return get_category_threads_pinned_category_query_hook(
        _get_category_threads_pinned_category_query_action,
        permissions,
        category,
        context,
    )


def _get_category_threads_pinned_category_query_action(
    permissions: UserPermissionsProxy, category: CategoryDict, context: str
) -> str | list[str] | None:
    if permissions.is_category_moderator(category["id"]):
        if context == CategoryQueryContext.CURRENT:
            return CategoryThreadsQuery.ALL_PINNED

        return CategoryThreadsQuery.ALL_PINNED_EVERYWHERE

    if permissions.user.is_authenticated:
        if context == CategoryQueryContext.CURRENT:
            return CategoryThreadsQuery.USER_PINNED

        return CategoryThreadsQuery.USER_PINNED_EVERYWHERE

    if context == CategoryQueryContext.CURRENT:
        return CategoryThreadsQuery.ANON_PINNED

    return CategoryThreadsQuery.ANON_PINNED_EVERYWHERE


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
            pinned__gt=ThreadPinned.NONE,
        )

    if query == CategoryThreadsQuery.ALL_PINNED_EVERYWHERE:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.EVERYWHERE,
        )

    if query == CategoryThreadsQuery.ALL_PINNED_CATEGORY:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.EVERYWHERE,
        )

    if query == CategoryThreadsQuery.ALL_NOT_PINNED:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.NONE,
        )

    if query == CategoryThreadsQuery.ALL_NOT_PINNED_EVERYWHERE:
        return Q(
            category_id__in=categories,
            pinned__lt=ThreadPinned.EVERYWHERE,
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
            pinned__gt=ThreadPinned.NONE,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_PINNED_EVERYWHERE:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.EVERYWHERE,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_PINNED_CATEGORY:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.CATEGORY,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_NOT_PINNED:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.NONE,
            is_hidden=False,
            is_unapproved=False,
        )

    if query == CategoryThreadsQuery.ANON_NOT_PINNED_EVERYWHERE:
        return Q(
            category_id__in=categories,
            pinned__lt=ThreadPinned.EVERYWHERE,
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
            pinned__gt=ThreadPinned.NONE,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_PINNED_EVERYWHERE:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.EVERYWHERE,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_PINNED_CATEGORY:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.CATEGORY,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_NOT_PINNED:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.NONE,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_NOT_PINNED_EVERYWHERE:
        return Q(
            category_id__in=categories,
            pinned__lt=ThreadPinned.EVERYWHERE,
            is_hidden=False,
        ) & Q(
            Q(is_unapproved=False) | Q(starter_id=user_id),
        )

    if query == CategoryThreadsQuery.USER_STARTED_PINNED:
        return Q(
            category_id__in=categories,
            pinned__gt=ThreadPinned.NONE,
            is_hidden=False,
            starter_id=user_id,
        )

    if query == CategoryThreadsQuery.USER_STARTED_PINNED_EVERYWHERE:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.EVERYWHERE,
            is_hidden=False,
            starter_id=user_id,
        )

    if query == CategoryThreadsQuery.USER_STARTED_PINNED_CATEGORY:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.CATEGORY,
            is_hidden=False,
            starter_id=user_id,
        )

    if query == CategoryThreadsQuery.USER_STARTED_NOT_PINNED:
        return Q(
            category_id__in=categories,
            pinned=ThreadPinned.NONE,
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


def filter_thread_updates_queryset(
    permissions: UserPermissionsProxy,
    thread: Thread,
    queryset: QuerySet,
):
    return filter_thread_updates_queryset_hook(
        _filter_thread_updates_queryset_action, permissions, thread, queryset
    )


def _filter_thread_updates_queryset_action(
    permissions: UserPermissionsProxy,
    thread: Thread,
    queryset: QuerySet,
):
    if permissions.is_category_moderator(thread.category_id):
        return queryset

    return queryset.filter(is_hidden=False)
