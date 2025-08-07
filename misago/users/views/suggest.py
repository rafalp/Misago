from functools import cmp_to_key

from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramWordSimilarity
from django.http import HttpRequest, JsonResponse

User = get_user_model()


def suggest_users(request: HttpRequest) -> JsonResponse:
    if query := request.GET.get("query", "").strip():
        results = find_users_suggestions(request, query)
    else:
        results = []

    return JsonResponse({"results": list(map(serialize_user, results))})


def find_users_suggestions(request: HttpRequest, query: str) -> list:
    exclude = []
    for user_id in request.GET.getlist("exclude")[:50]:
        try:
            user_id = int(user_id)
            if user_id and user_id not in exclude:
                exclude.append(user_id)
        except (TypeError, ValueError):
            pass

    results: list = []

    query_lower = query.lower()
    queryset = (
        User.objects.annotate(
            similarity=TrigramWordSimilarity(query, "username"),
        )
        .filter(is_active=True, similarity__gt=0.2)
        .order_by("-similarity")
    )

    if exclude:
        queryset = queryset.exclude(id__in=exclude)

    if request.user.is_authenticated and request.user.username == query_lower:
        results.append(request.user)
        queryset = queryset.exclude(id=request.user.id)

    elif exact_match := User.objects.filter(username=query).first():
        results.append(exact_match)
        queryset = queryset.exclude(id=exact_match.id).order_by()

    # Note: we can't do this filtering in queryset because it breaks similarity
    for result in queryset[:6]:
        if result.username.lower().startswith(query_lower):
            results.append(result)

    return sort_results(query, results)


def sort_results(query: str, results: list) -> list:
    query_lower = query.lower()
    lower_first = query_lower[0] == query[0]

    new_results = []

    # Put exact match first
    for i, result in enumerate(results[:]):
        if result.username == query:
            new_results.append(results.pop(i))
            break

    # Put case insensitive match first
    if not new_results:
        for i, result in enumerate(results[:]):
            if result.username.lower() == query_lower:
                new_results.append(results.pop(i))
                break

    def compare(item1: str, item2: str) -> bool:
        item1_len = len(item1.username)
        item2_len = len(item2.username)

        item1_lower = item1.username.lower()
        item2_lower = item2.username.lower()

        if lower_first:
            if (
                item1_lower[0] == item1.username[0]
                and item2_lower[0] != item2.username[0]
            ):
                return -1
            if (
                item2_lower[0] == item2.username[0]
                and item1_lower[0] != item1.username[0]
            ):
                return 1
        else:
            if (
                item1_lower[0] != item1.username[0]
                and item2_lower[0] == item2.username[0]
            ):
                return -1
            if (
                item2_lower[0] != item2.username[0]
                and item1_lower[0] == item1.username[0]
            ):
                return 1

        if item1_len < item2_len:
            return -1
        if item1_len > item2_len:
            return 1

        if item1.username < item2.username:
            return -1

        return 1

    return new_results + sorted(results, key=cmp_to_key(compare))


def serialize_user(user) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "slug": user.slug,
        "avatar": user.avatars,
    }
