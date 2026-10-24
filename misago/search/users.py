from typing import TYPE_CHECKING, Optional, TypedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from django.db.models.functions import Length

from ..core.utils import slugify
from ..permissions.proxy import UserPermissionsProxy

if TYPE_CHECKING:
    from ..users.models import User


class Stage(TypedDict):
    min_length: int
    prefix_length: int
    length_lt: int
    length_gt: int
    thresholds: list[tuple[int, int]]
    limit: int


class UserSearch:
    use_trigram_lookup: bool
    stages = list[Stage]

    def __init__(self, options: dict):
        self.use_trigram_lookup = bool(options.get("USE_TRIGRAM_LOOKUP"))

        self.stages = []
        for stage in options.get("STAGES", []):
            self.stages.append(self.get_stage_options(stage))

    def get_stage_options(self, stage: dict) -> Stage:
        min_length = max(int(stage.get("MIN_LENGTH", 0)), 1)
        prefix_length = max(int(stage.get("PREFIX_LENGTH", 0)), 0)
        if prefix_length:
            prefix_length = min(prefix_length, min_length)
        length_lt = max(int(stage.get("LENGTH_LT", 0)), 0)
        length_gt = max(int(stage.get("LENGTH_GT", 0)), 0)
        thresholds = sorted(
            ((l, t) for l, t in stage["THRESHOLDS"].items()),
            key=lambda i: i[0],
        )
        limit = max(int(stage.get("LIMIT", 0)), 1)

        return Stage(
            min_length=min_length,
            prefix_length=prefix_length,
            length_lt=length_lt,
            length_gt=length_gt,
            thresholds=thresholds,
            limit=limit,
        )

    def __call__(
        self,
        permissions: UserPermissionsProxy,
        username: str,
        include_deactivated: bool = False,
        include_self: bool = False,
    ) -> list["User"]:
        queryset = get_user_model().objects

        if not include_deactivated:
            queryset = queryset.filter(is_active=True)

        if not include_self and permissions.user.is_authenticated:
            queryset = queryset.exclude(id=permissions.user.id)

        results: list["User"] = []

        username = self.normalize_username(username)
        if not username:
            return results

        # First stage: search for exact match
        if exact_match := self.search_exact_match(queryset, username):
            results.append(exact_match)

        if self.use_trigram_lookup:
            queryset = queryset.filter(slug__trigram_similar=username)

        # Next stages
        for stage in self.stages:
            print(stage)
            results += self.search_matches(
                self.exclude_results(queryset, results), username, **stage
            )

        return results

    def normalize_username(self, username: str) -> str:
        return slugify(username)

    def search_exact_match(
        self, queryset: QuerySet["User"], username: str
    ) -> Optional["User"]:
        return queryset.filter(slug=username).first()

    def search_matches(
        self,
        queryset: QuerySet["User"],
        username: str,
        min_length: int,
        prefix_length: int,
        length_lt: int,
        length_gt: int,
        thresholds: list[tuple[int, float]],
        limit: int,
    ) -> list["User"]:
        if len(username) < min_length:
            return []

        queryset = self.search_prefix(queryset, username, prefix_length)
        queryset = self.search_length(queryset, username, length_lt, length_gt)
        queryset = self.search_similarity(queryset, username, thresholds)
        return list(queryset.order_by("-similarity")[:limit])

    def exclude_results(
        self, queryset: QuerySet["User"], exclude: list["User"]
    ) -> QuerySet["user"]:
        if exclude:
            return queryset.exclude(id__in=[user.id for user in exclude])

        return queryset

    def search_prefix(
        self, queryset: QuerySet["user"], username: str, prefix_length: int
    ) -> QuerySet["User"]:
        if prefix_length:
            print(username[:prefix_length])
            return queryset.filter(
                slug__startswith=username[:prefix_length],
            )

        return queryset.filter(
            slug__startswith=username,
        )

    def search_length(
        self, queryset: QuerySet["user"], username: str, lt: int, gt: int
    ) -> QuerySet["User"]:
        username_length = len(username)

        queryset = queryset.annotate(
            length=Length("slug"),
        )

        if not lt and not gt:
            return queryset.filter(length=username_length)

        return queryset.filter(
            length__gte=username_length - lt,
            length__lte=username_length + gt,
        )

    def search_similarity(
        self,
        queryset: QuerySet["user"],
        username: str,
        thresholds: list[tuple[int, int]],
    ) -> QuerySet["User"]:
        username_length = len(username)

        similarity = 0.3
        for threshold, threshold_similarity in thresholds:
            if username_length >= threshold:
                similarity = threshold_similarity

        return queryset.annotate(
            similarity=TrigramSimilarity("slug", username),
        ).filter(
            similarity__gte=similarity,
        )


search_users = UserSearch(settings.MISAGO_USERS_SEARCH)
