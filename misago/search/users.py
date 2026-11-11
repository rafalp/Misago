from functools import cmp_to_key
from typing import TYPE_CHECKING, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from django.db.models.functions import Length

from ..core.utils import slugify
from ..permissions.proxy import UserPermissionsProxy

if TYPE_CHECKING:
    from ..users.models import User


class UsersSearch:
    limit: int
    use_trigram_lookup: bool
    min_length: int
    min_similarity: float
    max_candidates: int
    max_differences: dict[int, int]

    def __init__(self, options: dict):
        self.limit = max(int(options.get("LIMIT", 0)), 3)
        self.use_trigram_lookup = bool(options.get("USE_TRIGRAM_LOOKUP"))
        self.min_length = max(int(options.get("MIN_LENGTH", 0)), 1)
        self.min_similarity = max(float(options.get("MIN_SIMILARITY", 0)), 0.1)
        self.max_candidates = max(int(options.get("MAX_CANDIDATES", 0)), 1)
        self.max_differences = options.get("MAX_DIFFERENCES", {})

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
            queryset = queryset.exclude(id=exact_match.id)

        if self.use_trigram_lookup:
            queryset = queryset.filter(slug__trigram_similar=username)

        results += self.search_candidates(queryset, username)
        results = self.remove_too_different_candidates(results, username)

        return self.sort_results(results, username)[: self.limit]

    def normalize_username(self, username: str) -> str:
        return slugify(username)

    def search_exact_match(
        self, queryset: QuerySet["User"], username: str
    ) -> Optional["User"]:
        return queryset.filter(slug=username).first()

    def search_candidates(
        self,
        queryset: QuerySet["User"],
        username: str,
    ) -> list["User"]:
        username_length = len(username)

        if username_length < self.min_length:
            return []

        queryset = (
            queryset.annotate(
                similarity=TrigramSimilarity("slug", username),
            )
            .filter(
                similarity__gte=self.min_similarity,
            )
            .order_by("similarity")
        )

        return list(queryset[: self.max_candidates])

    def remove_too_different_candidates(
        self, results: list["User"], username: str
    ) -> list["User"]:
        max_differences = 0

        username_length = len(username)
        for length, distance in self.max_differences.items():
            if length <= username_length:
                max_differences = distance

        filtered_results: list["User"] = []
        for result in results:
            if self.calc_difference(result.slug, username) <= max_differences:
                filtered_results.append(result)

        return filtered_results

    def calc_difference(self, a: str, b: str) -> int:
        if len(a) > len(b):
            a, b = b, a

        distance = 0
        for i, c in enumerate(a):
            if c != b[i]:
                distance += 1

        return distance

    def sort_results(self, results: list["User"], username: str) -> list["User"]:
        username_length = len(username)

        return sorted(
            results,
            key=cmp_to_key(
                lambda a, b: self.compare_results(a, b, username, username_length)
            ),
        )

    def compare_results(
        self, a: "User", b: "User", username: str, username_length: int
    ) -> int:
        # Exact match wins
        if a.slug == username:
            return -1
        if b.slug == username:
            return 1

        a_len = len(a.slug)
        b_len = len(b.slug)

        a_similarity = self.calc_similarity(username, a.slug)
        b_similarity = self.calc_similarity(username, b.slug)

        # Same length match for
        if a_len == b_len == username_length:
            # More similar match winds
            if a_similarity > b_similarity:
                return -1
            if a_similarity < b_similarity:
                return 1

        if a_len == username_length:
            return -1
        if b_len == username_length:
            return 1

        # Prefix match wins
        a_starts_with = a.slug.startswith(username)
        b_starts_with = b.slug.startswith(username)

        # If both matches start with search, shorter match wins
        if a_starts_with and b_starts_with:
            if a_len < b_len:
                return -1
            if a_len > b_len:
                return 1

        # Match that starts with search wins
        if a_starts_with:
            return -1
        if b_starts_with:
            return 1

        # Match with better prefix similarity wins
        if a_similarity > b_similarity:
            return -1
        if a_similarity < b_similarity:
            return 1

        # Shorter match wins
        if a_len < b_len:
            return -1
        if a_len > b_len:
            return 1

        return 0

    def calc_similarity(self, a: str, b: str) -> int:
        if len(a) > len(b):
            a, b = b, a

        similarity = []
        for i, c in enumerate(a):
            similarity.append(c == b[i])
        return sum(i if v else 0 for i, v in enumerate(reversed(similarity), 1))


search_users = UsersSearch(settings.MISAGO_USERS_SEARCH)
