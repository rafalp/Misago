from django.db.models import Q, QuerySet

from ...threads.enums import ThreadWeight
from ..enums import CategoryAccess, CategoryPermission
from ..hooks import get_category_access_level_hook
from ..proxy import UserPermissionsProxy


class ThreadsQuerysetFilter:
    def __call__(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        queryset: QuerySet,
    ) -> QuerySet:
        if permissions.is_global_moderator:
            return self.filter_queryset_for_global_moderator(
                permissions, categories, queryset
            )

        categories_access = get_categories_access(permissions, categories)
        filters: Q | None = self.get_queryset_filters(permissions, categories_access)

        if not filters:
            return queryset.none()

        return queryset.filter(filters)

    def filter_queryset_for_global_moderator(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        queryset: QuerySet,
    ) -> QuerySet:
        categories_ids: list[int] = []

        for category in categories:
            if _can_see_category_threads(permissions, category):
                categories_ids.append(category["id"])

        if categories_ids:
            return queryset.filter(category_id__in=categories_ids)

        return queryset.none()

    def get_queryset_filters(
        self,
        permissions: UserPermissionsProxy,
        access_levels: dict[str, list[int]],
    ) -> Q | None:
        filters: list[Q] = []
        for access_level, categories_ids in access_levels.items():
            if filter_ := self.get_access_level_filter(
                permissions, access_level, categories_ids
            ):
                filters.append(filter_)

        return _or_q(filters)

    def get_access_level_filter(
        self,
        permissions: UserPermissionsProxy,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        return None


class SitePinnedThreadsQuerysetFilter(ThreadsQuerysetFilter):
    def filter_queryset_for_global_moderator(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        queryset: QuerySet,
    ) -> QuerySet:
        return super().filter_queryset_for_global_moderator(
            permissions,
            categories,
            queryset.filter(weight=ThreadWeight.PINNED_GLOBALLY),
        )

    def get_access_level_filter(
        self,
        permissions: UserPermissionsProxy,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        if access_level == CategoryAccess.MODERATOR:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
            )

        if permissions.user.is_anonymous:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.PINNED_GLOBALLY,
                is_hidden=False,
                is_unapproved=False,
            )

        user_id = permissions.user.id
        return Q(
            category_id__in=categories_ids,
            weight=ThreadWeight.PINNED_GLOBALLY,
            is_hidden=False,
        ) & Q(Q(is_unapproved=False) | Q(starter_id=user_id))


class SiteThreadsQuerysetFilter(ThreadsQuerysetFilter):
    def filter_queryset_for_global_moderator(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        queryset: QuerySet,
    ) -> QuerySet:
        return super().filter_queryset_for_global_moderator(
            permissions,
            categories,
            queryset.filter(weight__lt=ThreadWeight.PINNED_GLOBALLY),
        )

    def get_access_level_filter(
        self,
        permissions: UserPermissionsProxy,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        if access_level == CategoryAccess.MODERATOR:
            return Q(
                category_id__in=categories_ids,
                weight__lt=ThreadWeight.PINNED_GLOBALLY,
            )

        if permissions.user.is_anonymous:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.PINNED_IN_CATEGORY,
                is_hidden=False,
                is_unapproved=False,
            )

        user_id = permissions.user.id
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
    def filter_queryset_for_global_moderator(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        queryset: QuerySet,
    ) -> QuerySet:
        return super().filter_queryset_for_global_moderator(
            permissions,
            categories,
            queryset.filter(weight__gt=ThreadWeight.NOT_PINNED),
        )

    def get_access_level_filter(
        self,
        permissions: UserPermissionsProxy,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        if access_level == CategoryAccess.MODERATOR:
            return Q(
                category_id__in=categories_ids,
                weight__gt=ThreadWeight.NOT_PINNED,
            )

        if permissions.user.is_anonymous:
            return Q(
                category_id__in=categories_ids,
                weight__gt=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                is_unapproved=False,
            )

        user_id = permissions.user.id
        return Q(
            category_id__in=categories_ids,
            weight__gt=ThreadWeight.NOT_PINNED,
            is_hidden=False,
        ) & Q(Q(is_unapproved=False) | Q(starter_id=user_id))


class CategoryThreadsQuerysetFilter(ThreadsQuerysetFilter):
    def filter_queryset_for_global_moderator(
        self,
        permissions: UserPermissionsProxy,
        categories: list[dict],
        queryset: QuerySet,
    ) -> QuerySet:
        return super().filter_queryset_for_global_moderator(
            permissions,
            categories,
            queryset.filter(weight=ThreadWeight.NOT_PINNED),
        )

    def get_access_level_filter(
        self,
        permissions: UserPermissionsProxy,
        access_level: str,
        categories_ids: list[int],
    ) -> Q | None:
        if access_level == CategoryAccess.MODERATOR:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.NOT_PINNED,
            )

        if permissions.user.is_anonymous:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.NOT_PINNED,
                is_hidden=False,
                is_unapproved=False,
            )

        user_id = permissions.user.id
        if access_level == CategoryAccess.DEFAULT:
            return Q(
                category_id__in=categories_ids,
                weight=ThreadWeight.NOT_PINNED,
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


filter_site_pinned_threads_queryset = SitePinnedThreadsQuerysetFilter()
filter_site_threads_queryset = SiteThreadsQuerysetFilter()

filter_category_pinned_threads_queryset = CategoryPinnedThreadsQuerysetFilter()
filter_category_threads_queryset = CategoryThreadsQuerysetFilter()


def get_categories_access(
    permissions: UserPermissionsProxy, categories: list[dict]
) -> dict[str, list[int]]:
    groups: dict[str, int] = {group: [] for group in CategoryAccess}

    for category in categories:
        if not _can_see_category_threads(permissions, category):
            continue

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


def _can_see_category_threads(
    permissions: UserPermissionsProxy, category: dict
) -> bool:
    return bool(
        category["id"] in permissions.categories[CategoryPermission.BROWSE]
        or (
            category["id"] in permissions.categories[CategoryPermission.SEE]
            and category["delay_browse_check"]
        )
    )


def _or_q(q: list[Q]):
    fin = None
    for cond in q:
        if fin is not None:
            fin |= cond
        else:
            fin = cond
    return fin
