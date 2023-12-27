from urllib.parse import urlencode

from django.urls import reverse

from ...test import assert_contains

ordering_link = reverse("misago:admin:groups:ordering")


def test_ordering_view_returns_error_405_if_request_is_not_post(admin_client):
    response = admin_client.get(ordering_link)
    assert response.status_code == 405


def test_ordering_view_returns_error_if_post_request_was_empty(admin_client):
    response = admin_client.post(ordering_link)
    assert_contains(response, "No items sent.", status_code=400)


def test_ordering_view_returns_error_if_posted_item_type_is_invalid(admin_client):
    response = admin_client.post(ordering_link, {"item": ["invalid"]})
    assert_contains(response, "Invalid item type: invalid", status_code=400)


def test_ordering_view_returns_error_if_posted_item_is_not_unique(
    admin_client, admins_group, members_group
):
    response = admin_client.post(
        ordering_link,
        {"item": [str(admins_group.id), str(members_group.id), str(members_group.id)]},
    )
    assert_contains(
        response,
        f"The item is not unique: {members_group.id}",
        status_code=400,
    )


def test_ordering_view_returns_error_if_posted_item_doesnt_exist(
    admin_client, admins_group, members_group
):
    response = admin_client.post(
        ordering_link,
        {
            "item": [
                str(admins_group.id),
                str(members_group.id),
                str(members_group.id + 100),
            ]
        },
    )
    assert_contains(
        response,
        f"The item does not exist: {members_group.id + 100}",
        status_code=400,
    )


def test_ordering_view_returns_204_response_on_success(
    admin_client, admins_group, moderators_group, members_group
):
    response = admin_client.post(
        ordering_link,
        {
            "item": [
                str(admins_group.id),
                str(moderators_group.id),
                str(members_group.id),
            ]
        },
    )
    assert response.status_code == 204
