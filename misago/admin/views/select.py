from django.contrib.auth import get_user_model
from django.shortcuts import render

from ...users.utils import slugify_username

User = get_user_model()

MAX_RESULTS = 10


def select_user(request):
    search = request.GET.get("search", "").strip()

    if search:
        username = slugify_username(search)
        choices = User.objects.filter(slug=username).union(
            User.objects.filter(slug__startswith=username)[:MAX_RESULTS]
        )
    else:
        choices = User.objects.none()

    return render(
        request, "misago/admin/select/user.html", {"search": search, "choices": choices}
    )
