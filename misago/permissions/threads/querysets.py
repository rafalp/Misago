from typing import Iterable

from django.db.models import Q, QuerySet

from ...threads.enums import ThreadWeight
from ..enums import CategoryAccess, CategoryPermission
from ..hooks import get_category_access_level_hook
from ..proxy import UserPermissionsProxy


class ThreadsQuerysetFilter:
    permissions: UserPermissionsProxy
    categories: list[dict]

    @classmethod
    def as_func(cls: "ThreadsQuerysetFilter"):
        def threads_queryset_filter_wrapper(
            permissions: UserPermissionsProxy,
            categories: list[dict],
            queryset: QuerySet,
        ):
            return cls(permissions, categories).filter(queryset)

        return threads_queryset_filter_wrapper

    def __init__(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
    ) -> QuerySet:
        self.permissions = permissions
        self.categories = []

        for category in categories:
            if category["id"] in permissions.categories[CategoryPermission.BROWSE] or (
                category["id"] in permissions.categories[CategoryPermission.SEE]
                and category["delay_browse_check"]
            ):
                self.categories.append(category)

    def filter(self, queryset: QuerySet) -> QuerySet:
        if self.permissions.is_global_moderator:
            return self.filter_queryset_for_global_moderator(queryset)

        categories_access = get_categories_access(self.permissions, self.categories)
        filters: Q | None = self.get_queryset_filters(categories_access)

        if not filters:
            return queryset.none()

        return queryset.filter(filters)

    def filter_queryset_for_global_moderator(self, queryset: QuerySet) -> QuerySet:
        categories_ids: list[int] = []
        for category in self.categories:
            categories_ids.append(category["id"])

        if categories_ids:
            return queryset.filter(category_id__in=categories_ids)

        return queryset.none()

    def get_queryset_filters(self, access_levels: dict[str, list[int]]) -> Q | None:
        filters: list[Q] = []
        for access_level, categories_ids in access_levels.items():
            if filter_ := self.get_access_level_filter(access_level, categories_ids):
                filters.append(filter_)

        return _or_q(filters)

    def get_access_level_filter(
        self, access_level: str, categories_ids: list[int]
    ) -> Q | None:
        return None


class SitePinnedThreadsQuerysetFilter(ThreadsQuerysetFilter):
    def filter_queryset_for_global_moderator(self, queryset: QuerySet) -> QuerySet:
        return super().filter_queryset_for_global_moderator(
            queryset.filter(weight=ThreadWeight.PINNED_GLOBALLY),
        )

    def get_access_level_filter(
        self,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        if access_level == CategoryAccess.MODERATOR:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
            )

        if self.permissions.user.is_anonymous:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
                is_unapproved=False,
            )

        user_id = self.permissions.user.id
        return Q(
            category_id__in=categories_ids,
            weight=ThreadWeight.PINNED_GLOBALLY,
            is_hidden=False,
        ) & Q(Q(is_unapproved=False) | Q(starter_id=user_id))


class SiteThreadsQuerysetFilter(ThreadsQuerysetFilter):
    def filter_queryset_for_global_moderator(self, queryset: QuerySet) -> QuerySet:
        return super().filter_queryset_for_global_moderator(
            queryset.filter(weight__lt=ThreadWeight.PINNED_GLOBALLY),
        )

    def get_access_level_filter(
        self,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        if access_level == CategoryAccess.MODERATOR:
            return Q(
                category_id__in=categories_ids,
                weight__lt=ThreadWeight.PINNED_GLOBALLY,
            )

        if self.permissions.user.is_anonymous:
            if access_level == CategoryAccess.DEFAULT:
                return Q(
                    category_id__in=categories_ids,
                    weight__lt=ThreadWeight.PINNED_GLOBALLY,
                    is_hidden=False,
                    is_unapproved=False,
                )

            if access_level == CategoryAccess.STARTED_ONLY:
                return Q(
                    category_id__in=categories_ids,
                    weight=ThreadWeight.PINNED_IN_CATEGORY,
                    is_hidden=False,
                    is_unapproved=False,
                )

        user_id = self.permissions.user.id
        if access_level == CategoryAccess.DEFAULT:
            return Q(
                category_id__in=categories_ids,
                weight__lt=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
            ) & Q(Q(is_unapproved=False) | Q(starter_id=user_id))

        if access_level == CategoryAccess.STARTED_ONLY:
            return Q(
                category_id__in=categories_ids,
                is_hidden=False,
            ) & (
                Q(
                    weight=ThreadWeight.PINNED_IN_CATEGORY,
                    is_unapproved=False,
                )
                | Q(
                    weight__lt=ThreadWeight.PINNED_GLOBALLY,
                    starter_id=user_id,
                )
            )


class CategoryThreadsQuerysetFilterMixin:
    permissions: UserPermissionsProxy
    current_category: dict
    child_categories: list[dict]
    include_children: bool

    @classmethod
    def as_func(cls: "ThreadsQuerysetFilter"):
        def threads_queryset_filter_wrapper(
            permissions: UserPermissionsProxy,
            categories: list[dict],
            queryset: QuerySet,
            *,
            current_category: dict,
            child_categories: list[dict],
            include_children: bool,
        ):
            return cls(
                permissions,
                categories,
                current_category,
                child_categories,
                include_children,
            ).filter(queryset)

        return threads_queryset_filter_wrapper

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
        self.child_categories = child_categories
        self.include_children = include_children

    def get_queryset_filters(self, access_levels: dict[str, list[int]]) -> Q | None:
        filters: list[Q] = []
        for access_level, categories_ids in access_levels.items():
            split_categories = self.split_categories_ids(categories_ids)
            if not any(split_categories):
                continue  # skip access level if there are valid categories for it

            if filter_ := self.get_access_level_filter(access_level, *split_categories):
                filters.append(filter_)

        return _or_q(filters)

    def split_categories_ids(
        self, categories_ids: list[int]
    ) -> tuple[int | None, list[int], list[int]]:
        current_id: int | None = None
        children_ids: list[int] = []
        other_ids: list[int] = []

        if self.current_category and self.current_category["id"] in categories_ids:
            current_id = self.current_category["id"]

        if self.child_categories:
            children_ids = [
                c["id"] for c in self.child_categories if c["id"] in categories_ids
            ]

        for category_id in categories_ids:
            if category_id != current_id and category_id not in children_ids:
                other_ids.append(category_id)

        if self.include_children:
            return current_id, children_ids, other_ids

        return current_id, [], other_ids

    def get_access_level_filter(
        self,
        access_level: str,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        if access_level == CategoryAccess.MODERATOR:
            return self.get_moderator_access_level_filter(
                current_id, children_ids, other_ids
            )

        if self.permissions.user.is_authenticated:
            if access_level == CategoryAccess.DEFAULT:
                return self.get_default_user_access_level_filter(
                    self.permissions.user.id, current_id, children_ids, other_ids
                )

            if access_level == CategoryAccess.STARTED_ONLY:
                return self.get_started_only_user_access_level_filter(
                    self.permissions.user.id, current_id, children_ids, other_ids
                )
        else:
            if access_level == CategoryAccess.DEFAULT:
                return self.get_default_anonymous_access_level_filter(
                    current_id, children_ids, other_ids
                )

            if access_level == CategoryAccess.STARTED_ONLY:
                return self.get_started_only_anonymous_access_level_filter(
                    current_id, children_ids, other_ids
                )

        return None

    def get_moderator_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        return None

    def get_default_user_access_level_filter(
        self,
        user_id: int,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        return None

    def get_default_anonymous_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        return None

    def get_started_only_user_access_level_filter(
        self,
        user_id: int,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        return None

    def get_started_only_anonymous_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        return None


class CategoryPinnedThreadsQuerysetFilter(
    CategoryThreadsQuerysetFilterMixin, ThreadsQuerysetFilter
):
    def filter_queryset_for_global_moderator(self, queryset: QuerySet) -> QuerySet:
        current_category_id = self.current_category["id"]
        filters = Q(
            category_id=current_category_id,
            weight__gt=ThreadWeight.NOT_PINNED,
        )

        other_categories_ids: list[int] = [
            c["id"] for c in self.categories if c["id"] != current_category_id
        ]

        if other_categories_ids:
            filters = filters | Q(
                category_id__in=other_categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
            )
            return queryset.filter(filters)

        return queryset.none()

    def get_moderator_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        current_category: Q | None = None
        other_categories: Q | None = None

        if current_id:
            current_category = Q(
                category_id=current_id,
                weight__gt=ThreadWeight.NOT_PINNED,
            )

        if children_ids or other_ids:
            other_categories = Q(
                category_id__in=children_ids + other_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
            )

        return _or_q((current_category, other_categories))

    def get_default_user_access_level_filter(
        self,
        user_id: int,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        current_category: Q | None = None
        other_categories: Q | None = None

        user_filters = Q(Q(is_unapproved=False) | Q(starter_id=user_id))

        if current_id:
            current_category = Q(
                category_id=current_id,
                weight__gt=ThreadWeight.NOT_PINNED,
                is_hidden=False,
            )

        if children_ids or other_ids:
            other_categories = Q(
                category_id__in=children_ids + other_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
            )

        return _or_q((current_category, other_categories)) & user_filters

    def get_default_anonymous_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        current_category: Q | None = None
        other_categories: Q | None = None

        if current_id:
            current_category = Q(
                category_id=current_id,
                weight__gt=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                is_unapproved=False,
            )

        if children_ids or other_ids:
            other_categories = Q(
                category_id__in=children_ids + other_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
                is_unapproved=False,
            )

        return _or_q((current_category, other_categories))

    get_started_only_user_access_level_filter = get_default_user_access_level_filter
    get_started_only_anonymous_access_level_filter = (
        get_default_anonymous_access_level_filter
    )


class CategoryThreadsQuerysetFilter(
    CategoryThreadsQuerysetFilterMixin, ThreadsQuerysetFilter
):
    def filter_queryset_for_global_moderator(self, queryset: QuerySet) -> QuerySet:
        if not self.include_children:
            return queryset.filter(category_id=self.current_category["id"])

        visible_categories: set[int] = set(c["id"] for c in self.categories)
        displayed_categories = set(
            [self.current_category["id"]] + [c["id"] for c in self.child_categories]
        )

        return queryset.filter(
            category_id__in=visible_categories.intersection(displayed_categories)
        )

    def get_moderator_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        if current_id and children_ids:
            return Q(
                category_id__in=[current_id] + children_ids,
                weight=ThreadWeight.NOT_PINNED,
            )

        if current_id:
            return Q(
                category_id=current_id,
                weight=ThreadWeight.NOT_PINNED,
            )

        if children_ids:
            return Q(
                category_id__in=children_ids,
                weight=ThreadWeight.NOT_PINNED,
            )

        return None

    def get_default_user_access_level_filter(
        self,
        user_id: int,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        current_category: Q | None = None
        children_categories: Q | None = None

        user_filters = Q(Q(is_unapproved=False) | Q(starter_id=user_id))

        if current_id:
            current_category = (
                Q(
                    category_id=current_id,
                    weight=ThreadWeight.NOT_PINNED,
                    is_hidden=False,
                )
                & user_filters
            )

        if children_ids:
            children_categories = (
                Q(
                    category_id__in=children_ids,
                    weight__lt=ThreadWeight.PINNED_GLOBALLY,
                    is_hidden=False,
                )
                & user_filters
            )

        return _or_q([current_category, children_categories])

    def get_default_anonymous_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        current_category: Q | None = None
        children_categories: Q | None = None

        if current_id:
            current_category = Q(
                category_id=current_id,
                weight=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                is_unapproved=False,
            )

        if children_ids:
            children_categories = Q(
                category_id__in=children_ids,
                weight__lt=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
                is_unapproved=False,
            )

        return _or_q([current_category, children_categories])

    def get_started_only_user_access_level_filter(
        self,
        user_id: int,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        not_pinned: Q | None = None
        pinned_in_children: Q | None = None

        if current_id and children_ids:
            not_pinned = Q(
                category_id__in=[current_id] + children_ids,
                weight=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                starter_id=user_id,
            )
        elif current_id:
            not_pinned = Q(
                category_id=current_id,
                weight=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                starter_id=user_id,
            )
        elif children_ids:
            not_pinned = Q(
                category_id__in=children_ids,
                weight=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                starter_id=user_id,
            )

        if children_ids:
            pinned_in_children = Q(
                category_id__in=children_ids,
                weight=ThreadWeight.PINNED_IN_CATEGORY,
                is_hidden=False,
            ) & Q(Q(is_unapproved=False) | Q(starter_id=user_id))

        return _or_q([not_pinned, pinned_in_children])

    def get_started_only_anonymous_access_level_filter(
        self,
        current_id: int | None,
        children_ids: list[int],
        other_ids: list[int],
    ) -> Q | None:
        current_category: Q | None = None
        children_categories: Q | None = None

        if current_id:
            current_category = Q(
                category_id=current_id,
                weight=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                is_unapproved=False,
            )

        if children_ids:
            children_categories = Q(
                category_id__in=children_ids,
                weight=ThreadWeight.PINNED_IN_CATEGORY,
                is_hidden=False,
                is_unapproved=False,
            )

        return _or_q([current_category, children_categories])


filter_site_pinned_threads_queryset = SitePinnedThreadsQuerysetFilter.as_func()
filter_site_threads_queryset = SiteThreadsQuerysetFilter.as_func()

filter_category_pinned_threads_queryset = CategoryPinnedThreadsQuerysetFilter.as_func()
filter_category_threads_queryset = CategoryThreadsQuerysetFilter.as_func()


def get_categories_access(
    permissions: UserPermissionsProxy, categories: list[dict]
) -> dict[str, list[int]]:
    groups: dict[str, int] = {}

    for category in categories:
        if access_level := get_category_access_level(permissions, category):
            groups.setdefault(access_level, []).append(category["id"])

    return groups


def get_category_access_level(
    permissions: UserPermissionsProxy, category: dict
) -> str | None:
    return get_category_access_level_hook(
        _get_category_access_level_action, permissions, category
    )


def _get_category_access_level_action(
    permissions: UserPermissionsProxy, category: dict
) -> str | None:
    if category["id"] in permissions.categories_moderator:
        return CategoryAccess.MODERATOR
    elif category["show_started_only"]:
        return CategoryAccess.STARTED_ONLY
    else:
        return CategoryAccess.DEFAULT

    return None


def _or_q(q: Iterable[Q]):
    fin = None
    for cond in q:
        if cond:
            if fin is not None:
                fin |= cond
            else:
                fin = cond
    return fin
