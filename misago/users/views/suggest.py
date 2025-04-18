from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramWordSimilarity
from django.http import HttpRequest, JsonResponse

from ...core.utils import slugify

User = get_user_model()


def suggest_users(request: HttpRequest) -> JsonResponse:
    if query := request.GET.get("q", "").strip():
        results = find_users_suggestions(request, query)
    else:
        results = []

    return JsonResponse({"results": list(map(serialize_user, results))})


def find_users_suggestions(request: HttpRequest, query: str) -> list:
    results: list = []

    query_lower = query.lower()
    queryset = (
        User.objects.annotate(
            similarity=TrigramWordSimilarity(query, "username"),
        )
        .filter(is_active=True, similarity__gt=0.2)
        .order_by("-similarity")
    )

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

    return results


def serialize_user(user) -> dict:
    return {
        "username": user.username,
        "slug": user.slug,
        "avatar": user.avatars,
    }
