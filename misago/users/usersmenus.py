from typing import List

from django.urls import reverse

from .models import Rank
from .pages import user_profile, usercp, users_list


def get_users_menus(request) -> dict:
    return {
        "userOptions": [],
        "userProfile": [],
        "usersLists": get_users_lists(request),
    }


def get_users_lists(request) -> List[dict]:
    links = []

    for section in users_list.get_sections(request):
        links.append({"name": str(section["name"]), "url": reverse(section["link"])})

    ranks_queryset = (
        Rank.objects.filter(is_tab=True).order_by("order").values("id", "name", "slug")
    )

    for rank in ranks_queryset:
        links.append(
            {
                "name": rank["name"],
                "url": reverse("misago:users-rank", kwargs={"slug": rank["slug"]}),
            }
        )

    return links
