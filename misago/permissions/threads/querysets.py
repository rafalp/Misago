from django.db.models import Q, QuerySet

from ...threads.enums import ThreadWeight
from ..enums import CategoryAccess, CategoryPermission
from ..hooks import get_category_access_level_hook
from ..proxy import UserPermissionsProxy


class ThreadsQuerysetFilter:
    permissions: UserPermissionsProxy
    categories: list[dict]
    current_category: dict | None
    child_categories: list[dict] | None

    @classmethod
    def as_func(cls: "ThreadsQuerysetFilter"):
        def threads_queryset_filter_wrapper(
            permissions: UserPermissionsProxy,
            categories: list[dict],
            queryset: QuerySet,
            *,
            current_category: dict | None = None,
            child_categories: list[dict] | None = None,
        ):
            return cls(
                permissions,
                categories,
                current_category,
                child_categories,
            ).filter(queryset)

        return threads_queryset_filter_wrapper

    def __init__(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        current_category: dict | None,
        child_categories: list[dict] | None,
    ) -> QuerySet:
        self.permissions = permissions
        self.categories = []
        self.current_category = current_category
        self.child_categories = child_categories

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


class CategoryPinnedThreadsQuerysetFilter(ThreadsQuerysetFilter):
    def filter_queryset_for_global_moderator(self, queryset: QuerySet) -> QuerySet:
        current_category_id = self.current_category["id"]
        filters = Q(
            category_id=current_category_id,
            weight__gt=ThreadWeight.NOT_PINNED,
        )

        other_categories_ids: list[int] = []
        for category in self.categories:
            if category["id"] != current_category_id:
                other_categories_ids.append(category["id"])

        if other_categories_ids:
            filters = filters | Q(
                category_id__in=other_categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
            )
            return queryset.filter(filters)

        return queryset.none()

    def get_access_level_filter(
        self,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        current_category_id = self.current_category["id"]
        other_categories_ids = [i for i in categories_ids if i != current_category_id]

        if access_level == CategoryAccess.MODERATOR:
            return Q(
                category_id=current_category_id,
                weight__gt=ThreadWeight.NOT_PINNED,
            ) | Q(
                category_id__in=other_categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
            )

        if self.permissions.user.is_anonymous:
            return Q(
                category_id=current_category_id,
                weight__gt=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                is_unapproved=False,
            ) | Q(
                category_id__in=other_categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
                is_unapproved=False,
            )

        user_id = self.permissions.user.id
        return (
            Q(
                category_id=current_category_id,
                weight__gt=ThreadWeight.NOT_PINNED,
                is_hidden=False,
            )
            | Q(
                category_id__in=other_categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
            )
        ) & Q(Q(is_unapproved=False) | Q(starter_id=user_id))


class CategoryThreadsQuerysetFilter(ThreadsQuerysetFilter):
    def filter_queryset_for_global_moderator(self, queryset: QuerySet) -> QuerySet:
        current_category_id = self.current_category["id"]
        filters = Q(
            category_id=current_category_id,
            weight=ThreadWeight.NOT_PINNED,
        )

        other_categories_ids: list[int] = []
        for category in self.child_categories:
            if category["id"] != current_category_id:
                other_categories_ids.append(category["id"])

        if other_categories_ids:
            filters = filters | Q(category_id__in=other_categories_ids)

        return queryset.filter(filters)

    def get_queryset_filters(self, access_levels: dict[str, list[int]]) -> Q | None:
        filters: list[Q] = []
        for access_level, categories_ids in access_levels.items():
            categories_ids_subset = [self.current_category["id"]]
            categories_ids_subset += [
                c["id"] for c in self.child_categories if c["id"] in categories_ids
            ]

            if filter_ := self.get_access_level_filter(
                access_level, categories_ids_subset
            ):
                filters.append(filter_)

        return _or_q(filters)

    def get_access_level_filter(
        self,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        current_category_id = categories_ids[0]
        children_categories_ids = categories_ids[1:]

        if access_level == CategoryAccess.MODERATOR:
            filters = Q(
                category_id=current_category_id,
                weight=ThreadWeight.NOT_PINNED,
            )

            if children_categories_ids:
                filters = filters | Q(
                    category_id__in=children_categories_ids,
                    weight__lt=ThreadWeight.PINNED_GLOBALLY,
                )

            return filters

        if self.permissions.user.is_anonymous:
            if access_level == CategoryAccess.DEFAULT:
                filters = Q(
                    category_id=current_category_id,
                    weight=ThreadWeight.NOT_PINNED,
                    is_hidden=False,
                    is_unapproved=False,
                )

                if children_categories_ids:
                    filters = filters | Q(
                        category_id__in=children_categories_ids,
                        weight__lt=ThreadWeight.PINNED_GLOBALLY,
                        is_hidden=False,
                        is_unapproved=False,
                    )

                return filters

            if access_level == CategoryAccess.STARTED_ONLY:
                return Q(
                    category_id__in=children_categories_ids,
                    weight=ThreadWeight.PINNED_IN_CATEGORY,
                    is_hidden=False,
                    is_unapproved=False,
                )

            return None

        user_id = self.permissions.user.id
        unapproved_or_author = Q(Q(is_unapproved=False) | Q(starter_id=user_id))

        if access_level == CategoryAccess.DEFAULT:
            filters = (
                Q(
                    category_id=current_category_id,
                    weight=ThreadWeight.NOT_PINNED,
                    is_hidden=False,
                )
                & unapproved_or_author
            )

            if children_categories_ids:
                filters = (
                    filters
                    | Q(
                        category_id__in=children_categories_ids,
                        weight__lt=ThreadWeight.PINNED_GLOBALLY,
                        is_hidden=False,
                    )
                    & unapproved_or_author
                )

            return filters

        if access_level == CategoryAccess.STARTED_ONLY:
            filters = Q(
                category_id=current_category_id,
                weight=ThreadWeight.NOT_PINNED,
                starter_id=user_id,
                is_hidden=False,
            )

            if children_categories_ids:
                filters = (
                    filters
                    | (
                        Q(
                            category_id__in=children_categories_ids,
                            weight=ThreadWeight.PINNED_IN_CATEGORY,
                            is_hidden=False,
                        )
                        & unapproved_or_author
                    )
                    | (
                        Q(
                            category_id__in=children_categories_ids,
                            weight=ThreadWeight.NOT_PINNED,
                            starter_id=user_id,
                            is_hidden=False,
                        )
                    )
                )

            return filters

        return None


filter_site_pinned_threads_queryset = SitePinnedThreadsQuerysetFilter.as_func()
filter_site_threads_queryset = SiteThreadsQuerysetFilter.as_func()

filter_category_pinned_threads_queryset = CategoryPinnedThreadsQuerysetFilter.as_func()
filter_category_threads_queryset = CategoryThreadsQuerysetFilter.as_func()


def get_categories_access(
    permissions: UserPermissionsProxy, categories: list[dict]
) -> dict[str, list[int]]:
    groups: dict[str, int] = {group: [] for group in CategoryAccess}

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

    return CategoryAccess.DEFAULT


def _or_q(q: list[Q]):
    fin = None
    for cond in q:
        if fin is not None:
            fin |= cond
        else:
            fin = cond
    return fin
