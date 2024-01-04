import pytest

from ....acl.models import Role
from ....test import assert_contains, assert_not_contains
from ...models import Rank
from ...test import create_test_user


@pytest.fixture
def user_a(db):
    return create_test_user("Tyrael", "test123@test.org")


@pytest.fixture
def user_b(db):
    return create_test_user("Tyrion", "test321@gmail.com")


@pytest.fixture
def user_c(db):
    return create_test_user("Karen", "other432@gmail.com")


def test_search_finds_user_by_username(admin_client, users_admin_link, user_a):
    response = admin_client.get(f"{users_admin_link}&username=Tyrael")
    assert_contains(response, user_a.username)


def test_search_finds_user_by_username_with_underscore(
    admin_client, users_admin_link, other_user
):
    response = admin_client.get(f"{users_admin_link}&username=other_user")
    assert_contains(response, other_user.username)


def test_search_excludes_users_with_different_username(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get(f"{users_admin_link}&username=Tyrael")
    assert_not_contains(response, user_b.username)
    assert_not_contains(response, user_c.username)


def test_search_finds_users_by_username_start(
    admin_client, users_admin_link, user_a, user_b
):
    response = admin_client.get(f"{users_admin_link}&username=Tyr*")
    assert_contains(response, user_a.username)
    assert_contains(response, user_b.username)


def test_search_finds_user_username_with_underscore_by_username_start(
    admin_client, users_admin_link, other_user
):
    response = admin_client.get(f"{users_admin_link}&username=other_*")
    assert_contains(response, other_user.username)


def test_search_by_username_start_excludes_users_with_different_username(
    admin_client, users_admin_link, user_c
):
    response = admin_client.get(f"{users_admin_link}&username=Tyr*")
    assert_not_contains(response, user_c.username)


def test_search_finds_user_by_username_end(admin_client, users_admin_link, user_a):
    response = admin_client.get(f"{users_admin_link}&username=*ael")
    assert_contains(response, user_a.username)


def test_search_by_username_end_excludes_users_with_different_username(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get(f"{users_admin_link}&username=*ael")
    assert_not_contains(response, user_b.username)
    assert_not_contains(response, user_c.username)


def test_search_finds_users_by_username_content(
    admin_client, users_admin_link, user_a, user_b
):
    response = admin_client.get(f"{users_admin_link}&username=*yr*")
    assert_contains(response, user_a.username)
    assert_contains(response, user_b.username)


def test_search_by_username_content_excludes_users_with_different_username(
    admin_client, users_admin_link, user_c
):
    response = admin_client.get(f"{users_admin_link}&username=*yr*")
    assert_not_contains(response, user_c.username)


def test_search_finds_user_by_email(admin_client, users_admin_link, user_a):
    response = admin_client.get(f"{users_admin_link}&email=test123@test.org")
    assert_contains(response, user_a.email)


def test_search_excludes_users_with_different_email(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get(f"{users_admin_link}&email=test123@test.org")
    assert_not_contains(response, user_b.email)
    assert_not_contains(response, user_c.email)


def test_search_finds_users_by_email_start(
    admin_client, users_admin_link, user_a, user_b
):
    response = admin_client.get(f"{users_admin_link}&email=test*")
    assert_contains(response, user_a.email)
    assert_contains(response, user_b.email)


def test_search_by_email_start_excludes_users_with_different_email(
    admin_client, users_admin_link, user_c
):
    response = admin_client.get(f"{users_admin_link}&email=test*")
    assert_not_contains(response, user_c.email)


def test_search_finds_user_by_email_end(admin_client, users_admin_link, user_a):
    response = admin_client.get(f"{users_admin_link}&email=*org")
    assert_contains(response, user_a.email)


def test_search_by_email_end_excludes_users_with_different_email(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get(f"{users_admin_link}&email=*org")
    assert_not_contains(response, user_b.email)
    assert_not_contains(response, user_c.email)


def test_search_finds_users_by_email_content(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get(f"{users_admin_link}&email=*@gmail*")
    assert_contains(response, user_b.email)
    assert_contains(response, user_c.email)


def test_search_by_email_content_excludes_users_with_different_email(
    admin_client, users_admin_link, user_a
):
    response = admin_client.get(f"{users_admin_link}&email=*@gmail*")
    assert_not_contains(response, user_a.email)


def test_search_finds_user_with_main_group(
    admin_client, users_admin_link, other_user, members_group
):
    response = admin_client.get(f"{users_admin_link}&main_group={members_group.id}")
    assert_contains(response, other_user.username)


def test_staff_users_search_excludes_user_without_main_group(
    admin_client, users_admin_link, other_user, moderators_group
):
    response = admin_client.get(f"{users_admin_link}&main_group={moderators_group.id}")
    assert_not_contains(response, other_user.username)


def test_search_finds_user_with_group(
    admin_client, users_admin_link, other_user, moderators_group, members_group
):
    other_user.set_groups(members_group, [moderators_group])
    other_user.save()

    response = admin_client.get(f"{users_admin_link}&group={moderators_group.id}")
    assert_contains(response, other_user.username)


def test_staff_users_search_excludes_user_without_group(
    admin_client, users_admin_link, other_user, moderators_group
):
    response = admin_client.get(f"{users_admin_link}&group={moderators_group.id}")
    assert_not_contains(response, other_user.username)


@pytest.fixture
def rank(db):
    return Rank.objects.create(name="Test Rank")


def test_search_finds_user_with_rank(admin_client, users_admin_link, rank):
    user = create_test_user("UserWithRank", "rank@example.org", rank=rank)
    response = admin_client.get(f"{users_admin_link}&rank={rank.pk}")
    assert_contains(response, user.username)


def test_staff_users_search_excludes_user_without_rank(
    admin_client, users_admin_link, rank
):
    user = create_test_user("RegularUser", "regular@example.org")
    response = admin_client.get(f"{users_admin_link}&rank={rank.pk}")
    assert_not_contains(response, user.username)


@pytest.fixture
def role(db):
    return Role.objects.create(name="Test Role")


def test_search_finds_user_with_role(admin_client, users_admin_link, role):
    user = create_test_user("UserWithRole", "role@example.org")
    user.roles.add(role)

    response = admin_client.get(f"{users_admin_link}&role={role.pk}")
    assert_contains(response, user.username)


def test_staff_users_search_excludes_user_without_role(
    admin_client, users_admin_link, role
):
    user = create_test_user("RegularUser", "regular@example.org")
    response = admin_client.get(f"{users_admin_link}&role={role.pk}")
    assert_not_contains(response, user.username)


def test_search_finds_inactive_user(admin_client, users_admin_link):
    user = create_test_user(
        "InactiveUser", "inactive@example.org", requires_activation=1
    )
    response = admin_client.get(f"{users_admin_link}&is_inactive=1")
    assert_contains(response, user.username)


def test_inactive_users_search_excludes_activated_users(admin_client, users_admin_link):
    user = create_test_user(
        "ActivatedUser", "activated@example.org", requires_activation=0
    )
    response = admin_client.get(f"{users_admin_link}&is_inactive=1")
    assert_not_contains(response, user.username)


def test_search_finds_deactivated_user(admin_client, users_admin_link):
    user = create_test_user("DisabledUser", "disabled@example.org", is_active=False)
    response = admin_client.get(f"{users_admin_link}&is_deactivated=1")
    assert_contains(response, user.username)


def test_deactivated_users_search_excludes_active_users(admin_client, users_admin_link):
    user = create_test_user("ActiveUser", "active@example.org", is_active=True)
    response = admin_client.get(f"{users_admin_link}&is_deactivated=1")
    assert_not_contains(response, user.username)


def test_search_finds_root_admin_user(admin_client, users_admin_link, root_admin):
    response = admin_client.get(f"{users_admin_link}&is_admin=1")
    assert_contains(response, root_admin.username)


def test_search_finds_admin_user(admin_client, users_admin_link, other_admin):
    response = admin_client.get(f"{users_admin_link}&is_admin=1")
    assert_contains(response, other_admin.username)


def test_search_finds_secondary_admin_user(
    admin_client, users_admin_link, secondary_admin
):
    response = admin_client.get(f"{users_admin_link}&is_admin=1")
    assert_contains(response, secondary_admin.username)


def test_admin_users_search_excludes_non_admin_users(
    admin_client, users_admin_link, other_user
):
    response = admin_client.get(f"{users_admin_link}&is_admin=1")
    assert_not_contains(response, other_user.username)


def test_search_finds_user_deleting_account(admin_client, users_admin_link):
    user = create_test_user(
        "DeletingUser", "deleting@example.org", is_deleting_account=True
    )
    response = admin_client.get(f"{users_admin_link}&is_deleting_account=1")
    assert_contains(response, user.username)


def test_staff_users_search_excludes_non_deleting_users(admin_client, users_admin_link):
    user = create_test_user(
        "RegularUser", "regular@example.org", is_deleting_account=False
    )
    response = admin_client.get(f"{users_admin_link}&is_deleting_account=1")
    assert_not_contains(response, user.username)
