import pytest
from django.urls import reverse

from ....admin.test import AdminTestCase
from ....test import assert_contains
from ...models import Agreement


@pytest.fixture
def list_url(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:agreements:index"))
    return response["location"]


@pytest.fixture
def agreement(superuser):
    return Agreement.objects.create(
        type=Agreement.TYPE_TOS,
        title="Test TOS",
        link="https://rules.com",
        created_by=superuser,
        created_by_name=superuser.username,
    )


@pytest.fixture
def active_agreement(agreement):
    agreement.is_active = True
    agreement.save()
    return agreement


@pytest.fixture
def other_agreement(superuser):
    return Agreement.objects.create(
        type=Agreement.TYPE_TOS,
        title="Test TOS",
        link="https://rules.com",
        created_by=superuser,
        created_by_name=superuser.username,
    )


def test_nav_contains_agreements_link(admin_client, list_url):
    response = admin_client.get(list_url)
    assert_contains(response, reverse("misago:admin:settings:agreements:index"))


def test_empty_list_renders(admin_client, list_url):
    response = admin_client.get(list_url)
    assert response.status_code == 200


def test_list_renders_agreement(admin_client, list_url, agreement):
    response = admin_client.get(list_url)
    assert_contains(response, agreement.title)


def test_agreements_can_be_mass_deleted(admin_client, list_url, superuser):
    agreements = []
    for _ in range(10):
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            title="Test TOS",
            link="https://rules.com",
            created_by=superuser,
            created_by_name=superuser.username,
        )
        agreements.append(agreement.pk)

    response = admin_client.post(
        list_url, data={"action": "delete", "selected_items": agreements}
    )
    assert response.status_code == 302
    assert Agreement.objects.count() == 0


def test_creation_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:agreements:new"))
    assert response.status_code == 200


def test_form_creates_new_agreement(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:agreements:new"),
        {
            "type": Agreement.TYPE_TOS,
            "title": "Test TOS",
            "text": "Lorem ipsum dolor met sit amet elit",
            "link": "https://example.com/rules/",
        },
    )

    agreement = Agreement.objects.get()
    assert agreement.type == Agreement.TYPE_TOS
    assert agreement.title == "Test TOS"
    assert agreement.text == "Lorem ipsum dolor met sit amet elit"
    assert agreement.link == "https://example.com/rules/"


def test_form_sets_new_agreement_creator(admin_client, superuser):
    response = admin_client.post(
        reverse("misago:admin:settings:agreements:new"),
        {
            "type": Agreement.TYPE_TOS,
            "title": "Test TOS",
            "text": "Lorem ipsum dolor met sit amet elit",
            "link": "https://example.com/rules/",
        },
    )

    agreement = Agreement.objects.get()
    assert agreement.created_by == superuser
    assert agreement.created_by_name == superuser.username


def test_form_creates_active_agreement(mocker, admin_client):
    set_agreement_as_active = mocker.patch(
        "misago.legal.admin.forms.set_agreement_as_active"
    )
    response = admin_client.post(
        reverse("misago:admin:settings:agreements:new"),
        {
            "type": Agreement.TYPE_TOS,
            "is_active": "1",
            "title": "Test TOS",
            "text": "Lorem ipsum dolor met sit amet elit",
            "link": "https://example.com/rules/",
        },
    )

    agreement = Agreement.objects.get()
    assert agreement.is_active
    set_agreement_as_active.assert_called_once_with(agreement)


def test_newly_created_active_agreement_replaces_current_one(
    admin_client, active_agreement
):
    response = admin_client.post(
        reverse("misago:admin:settings:agreements:new"),
        {
            "type": Agreement.TYPE_TOS,
            "is_active": "1",
            "title": "Test TOS",
            "text": "Lorem ipsum dolor met sit amet elit",
            "link": "https://example.com/rules/",
        },
    )

    agreement = Agreement.objects.exclude(pk=active_agreement.pk).get()
    assert agreement.is_active

    active_agreement.refresh_from_db()
    assert not active_agreement.is_active


def test_edit_form_renders(admin_client, agreement):
    response = admin_client.get(
        reverse("misago:admin:settings:agreements:edit", kwargs={"pk": agreement.pk})
    )
    assert_contains(response, agreement.title)


def test_edit_form_updates_agreement(admin_client, agreement):
    response = admin_client.post(
        reverse("misago:admin:settings:agreements:edit", kwargs={"pk": agreement.pk}),
        data={
            "type": Agreement.TYPE_TOS,
            "title": "Test Edited",
            "text": "Sit amet elit",
            "link": "https://example.com/terms/",
        },
    )
    assert response.status_code == 302

    agreement.refresh_from_db()
    assert agreement.type == Agreement.TYPE_TOS
    assert agreement.title == "Test Edited"
    assert agreement.text == "Sit amet elit"
    assert agreement.link == "https://example.com/terms/"


def test_edit_form_updates_agreement_modified_entry(admin_client, agreement, superuser):
    response = admin_client.post(
        reverse("misago:admin:settings:agreements:edit", kwargs={"pk": agreement.pk}),
        data={
            "type": Agreement.TYPE_TOS,
            "title": "Test Edited",
            "text": "Sit amet elit",
            "link": "https://example.com/terms/",
        },
    )
    assert response.status_code == 302

    agreement.refresh_from_db()
    assert agreement.last_modified_on
    assert agreement.last_modified_by == superuser
    assert agreement.last_modified_by_name == superuser.username


def test_edit_form_changes_active_agreement(
    admin_client, active_agreement, other_agreement
):
    response = admin_client.post(
        reverse(
            "misago:admin:settings:agreements:edit", kwargs={"pk": other_agreement.pk}
        ),
        data={
            "type": Agreement.TYPE_TOS,
            "is_active": "1",
            "title": "Test Edited",
            "text": "Sit amet elit",
            "link": "https://example.com/terms/",
        },
    )
    assert response.status_code == 302

    active_agreement.refresh_from_db()
    assert not active_agreement.is_active

    other_agreement.refresh_from_db()
    assert other_agreement.is_active


def test_edit_form_disables_active_agreement(admin_client, active_agreement):
    response = admin_client.post(
        reverse(
            "misago:admin:settings:agreements:edit", kwargs={"pk": active_agreement.pk}
        ),
        data={
            "type": Agreement.TYPE_TOS,
            "is_active": "0",
            "title": "Test Edited",
            "text": "Sit amet elit",
            "link": "https://example.com/terms/",
        },
    )
    assert response.status_code == 302

    active_agreement.refresh_from_db()
    assert not active_agreement.is_active


def test_agreement_can_be_deleted(admin_client, agreement):
    response = admin_client.post(
        reverse("misago:admin:settings:agreements:delete", kwargs={"pk": agreement.pk})
    )
    assert response.status_code == 302

    with pytest.raises(Agreement.DoesNotExist):
        agreement.refresh_from_db()


def test_active_agreement_can_be_deleted(admin_client, active_agreement):
    response = admin_client.post(
        reverse(
            "misago:admin:settings:agreements:delete",
            kwargs={"pk": active_agreement.pk},
        )
    )
    assert response.status_code == 302

    with pytest.raises(Agreement.DoesNotExist):
        active_agreement.refresh_from_db()


def test_agreement_can_be_set_as_active(admin_client, agreement):
    response = admin_client.post(
        reverse(
            "misago:admin:settings:agreements:set-as-active",
            kwargs={"pk": agreement.pk},
        )
    )
    assert response.status_code == 302

    agreement.refresh_from_db()
    assert agreement.is_active


def test_active_agreement_can_be_changed(
    admin_client, active_agreement, other_agreement
):
    response = admin_client.post(
        reverse(
            "misago:admin:settings:agreements:set-as-active",
            kwargs={"pk": other_agreement.pk},
        )
    )
    assert response.status_code == 302

    active_agreement.refresh_from_db()
    assert not active_agreement.is_active

    other_agreement.refresh_from_db()
    assert other_agreement.is_active


def test_active_agreement_can_be_disabled(admin_client, active_agreement):
    response = admin_client.post(
        reverse(
            "misago:admin:settings:agreements:disable",
            kwargs={"pk": active_agreement.pk},
        )
    )
    assert response.status_code == 302

    active_agreement.refresh_from_db()
    assert not active_agreement.is_active
