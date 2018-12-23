from django.contrib.auth import get_user_model
from django.contrib.staticfiles.templatetags.staticfiles import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ...conf import settings

User = get_user_model()


@api_view()
def mention_suggestions(request):
    suggestions = []

    query = request.query_params.get("q", "").lower().strip()[:100]
    if query:
        queryset = User.objects.filter(slug__startswith=query, is_active=True).order_by(
            "slug"
        )[:10]

        for user in queryset:
            try:
                avatar = user.avatars[-1]["url"]
            except IndexError:
                avatar = static(settings.MISAGO_BLANK_AVATAR)

            suggestions.append({"username": user.username, "avatar": avatar})

    return Response(suggestions)
