from django.urls import reverse

from ...test import assert_contains


def test_threads_search_view_returns_error_403_if_user_cant_search(user_client, user):
    user.group.can_search = False
    user.group.save()

    response = user_client.get(reverse("misago:threads-search"))
    assert_contains(response, "You can&#x27;t search this site.", status_code=403)
