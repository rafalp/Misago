import json

import pytest
from django.urls import reverse

from ...users.test import AuthenticatedUserTestCase
from ..models import Agreement


@pytest.fixture
def agreement(db):
    return Agreement.objects.create(
        type=Agreement.TYPE_TOS,
        text="Lorem ipsum",
        is_active=True,
    )


def test_submit_agreement_api_returns_403_error_if_user_is_anonymous(client, agreement):
    response = client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
    )
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "This action is not available to guests.",
    }


def test_submit_agreement_api_returns_405_error_if_request_method_is_get(
    client, agreement
):
    response = client.get(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
    )
    assert response.status_code == 405
    assert json.loads(response.content) == {"detail": 'Method "GET" not allowed.'}


def test_submit_agreement_api_returns_404_error_if_agreement_id_is_invalid(
    user_client, agreement
):
    response = user_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id + 1}),
    )
    assert response.status_code == 404
    assert json.loads(response.content) == {"detail": "Not found."}


def test_submit_agreement_api_returns_403_error_if_agreement_was_already_accepted(
    user_client, user, agreement
):
    user.agreements.append(agreement.id)
    user.save()

    response = user_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
    )
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "You have already accepted this agreement.",
    }


def test_submit_agreement_api_returns_403_error_if_request_was_missing_payload(
    user_client, agreement
):
    response = user_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
    )
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "You need to submit a valid choice.",
    }


def test_submit_agreement_api_returns_403_error_if_request_payload_was_invalid(
    user_client, agreement
):
    response = user_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
        json={"accept": 1},
    )
    assert response.status_code == 403
    assert json.loads(response.content) == {
        "detail": "You need to submit a valid choice.",
    }


def test_submit_agreement_api_records_user_acceptance(user_client, user, agreement):
    response = user_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
        json={"accept": True},
    )
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.agreements == [agreement.id]
    assert user.is_active
    assert not user.is_deleting_account


def test_submit_agreement_api_marks_user_for_deletion_on_rejection(
    user_client, user, agreement
):
    response = user_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
        json={"accept": False},
    )
    assert response.status_code == 200

    user.refresh_from_db()
    assert not user.is_active
    assert user.is_deleting_account


def test_submit_agreement_api_allows_staff_reject_agreement(
    staff_client, staffuser, agreement
):
    response = staff_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
        json={"accept": False},
    )
    assert response.status_code == 200

    staffuser.refresh_from_db()
    assert staffuser.is_active
    assert not staffuser.is_deleting_account


def test_submit_agreement_api_allows_admin_reject_agreement(
    admin_client, admin, agreement
):
    response = admin_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
        json={"accept": False},
    )
    assert response.status_code == 200

    admin.refresh_from_db()
    assert admin.is_active
    assert not admin.is_deleting_account


def test_submit_agreement_api_allows_root_admin_reject_agreement(
    root_admin_client, root_admin, agreement
):
    response = root_admin_client.post(
        reverse("misago:api:submit-agreement", kwargs={"pk": agreement.id}),
        json={"accept": False},
    )
    assert response.status_code == 200

    root_admin.refresh_from_db()
    assert root_admin.is_active
    assert not root_admin.is_deleting_account
