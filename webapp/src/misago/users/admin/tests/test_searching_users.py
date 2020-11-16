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
    response = admin_client.get("%s&username=Tyrael" % users_admin_link)
    assert_contains(response, user_a.username)


def test_search_excludes_users_with_different_username(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get("%s&username=Tyrael" % users_admin_link)
    assert_not_contains(response, user_b.username)
    assert_not_contains(response, user_c.username)


def test_search_finds_users_by_username_start(
    admin_client, users_admin_link, user_a, user_b
):
    response = admin_client.get("%s&username=Tyr*" % users_admin_link)
    assert_contains(response, user_a.username)
    assert_contains(response, user_b.username)


def test_search_by_username_start_excludes_users_with_different_username(
    admin_client, users_admin_link, user_c
):
    response = admin_client.get("%s&username=Tyr*" % users_admin_link)
    assert_not_contains(response, user_c.username)


def test_search_finds_user_by_username_end(admin_client, users_admin_link, user_a):
    response = admin_client.get("%s&username=*ael" % users_admin_link)
    assert_contains(response, user_a.username)


def test_search_by_username_end_excludes_users_with_different_username(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get("%s&username=*ael" % users_admin_link)
    assert_not_contains(response, user_b.username)
    assert_not_contains(response, user_c.username)


def test_search_finds_users_by_username_content(
    admin_client, users_admin_link, user_a, user_b
):
    response = admin_client.get("%s&username=*yr*" % users_admin_link)
    assert_contains(response, user_a.username)
    assert_contains(response, user_b.username)


def test_search_by_username_content_excludes_users_with_different_username(
    admin_client, users_admin_link, user_c
):
    response = admin_client.get("%s&username=*yr*" % users_admin_link)
    assert_not_contains(response, user_c.username)


def test_search_finds_user_by_email(admin_client, users_admin_link, user_a):
    response = admin_client.get("%s&email=test123@test.org" % users_admin_link)
    assert_contains(response, user_a.email)


def test_search_excludes_users_with_different_email(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get("%s&email=test123@test.org" % users_admin_link)
    assert_not_contains(response, user_b.email)
    assert_not_contains(response, user_c.email)


def test_search_finds_users_by_email_start(
    admin_client, users_admin_link, user_a, user_b
):
    response = admin_client.get("%s&email=test*" % users_admin_link)
    assert_contains(response, user_a.email)
    assert_contains(response, user_b.email)


def test_search_by_email_start_excludes_users_with_different_email(
    admin_client, users_admin_link, user_c
):
    response = admin_client.get("%s&email=test*" % users_admin_link)
    assert_not_contains(response, user_c.email)


def test_search_finds_user_by_email_end(admin_client, users_admin_link, user_a):
    response = admin_client.get("%s&email=*org" % users_admin_link)
    assert_contains(response, user_a.email)


def test_search_by_email_end_excludes_users_with_different_email(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get("%s&email=*org" % users_admin_link)
    assert_not_contains(response, user_b.email)
    assert_not_contains(response, user_c.email)


def test_search_finds_users_by_email_content(
    admin_client, users_admin_link, user_b, user_c
):
    response = admin_client.get("%s&email=*@gmail*" % users_admin_link)
    assert_contains(response, user_b.email)
    assert_contains(response, user_c.email)


def test_search_by_email_content_excludes_users_with_different_email(
    admin_client, users_admin_link, user_a
):
    response = admin_client.get("%s&email=*@gmail*" % users_admin_link)
    assert_not_contains(response, user_a.email)


@pytest.fixture
def rank(db):
    return Rank.objects.create(name="Test Rank")


def test_search_finds_user_with_rank(admin_client, users_admin_link, rank):
    user = create_test_user("UserWithRank", "rank@example.org", rank=rank)
    response = admin_client.get("%s&rank=%s" % (users_admin_link, rank.pk))
    assert_contains(response, user.username)


def test_staff_users_search_excludes_user_without_rank(
    admin_client, users_admin_link, rank
):
    user = create_test_user("RegularUser", "regular@example.org")
    response = admin_client.get("%s&rank=%s" % (users_admin_link, rank.pk))
    assert_not_contains(response, user.username)


@pytest.fixture
def role(db):
    return Role.objects.create(name="Test Role")


def test_search_finds_user_with_role(admin_client, users_admin_link, role):
    user = create_test_user("UserWithRole", "role@example.org")
    user.roles.add(role)
    response = admin_client.get("%s&role=%s" % (users_admin_link, role.pk))
    assert_contains(response, user.username)


def test_staff_users_search_excludes_user_without_role(
    admin_client, users_admin_link, role
):
    user = create_test_user("RegularUser", "regular@example.org")
    response = admin_client.get("%s&role=%s" % (users_admin_link, role.pk))
    assert_not_contains(response, user.username)


def test_search_finds_inactive_user(admin_client, users_admin_link):
    user = create_test_user(
        "InactiveUser", "inactive@example.org", requires_activation=1
    )
    response = admin_client.get("%s&is_inactive=1" % users_admin_link)
    assert_contains(response, user.username)


def test_inactive_users_search_excludes_activated_users(admin_client, users_admin_link):
    user = create_test_user(
        "ActivatedUser", "activated@example.org", requires_activation=0
    )
    response = admin_client.get("%s&is_inactive=1" % users_admin_link)
    assert_not_contains(response, user.username)


def test_search_finds_disabled_user(admin_client, users_admin_link):
    user = create_test_user("DisabledUser", "disabled@example.org", is_active=False)
    response = admin_client.get("%s&is_disabled=1" % users_admin_link)
    assert_contains(response, user.username)


def test_disabled_users_search_excludes_active_users(admin_client, users_admin_link):
    user = create_test_user("ActiveUser", "active@example.org", is_active=True)
    response = admin_client.get("%s&is_disabled=1" % users_admin_link)
    assert_not_contains(response, user.username)


def test_search_finds_staff_user(admin_client, users_admin_link):
    user = create_test_user("StaffUser", "staff@example.org", is_staff=True)
    response = admin_client.get("%s&is_staff=1" % users_admin_link)
    assert_contains(response, user.username)


def test_staff_users_search_excludes_non_staff_users(admin_client, users_admin_link):
    user = create_test_user("RegularUser", "non_staff@example.org", is_staff=False)
    response = admin_client.get("%s&is_staff=1" % users_admin_link)
    assert_not_contains(response, user.username)


def test_search_finds_user_deleting_account(admin_client, users_admin_link):
    user = create_test_user(
        "DeletingUser", "deleting@example.org", is_deleting_account=True
    )
    response = admin_client.get("%s&is_deleting_account=1" % users_admin_link)
    assert_contains(response, user.username)


def test_staff_users_search_excludes_non_deleting_users(admin_client, users_admin_link):
    user = create_test_user(
        "RegularUser", "regular@example.org", is_deleting_account=False
    )
    response = admin_client.get("%s&is_deleting_account=1" % users_admin_link)
    assert_not_contains(response, user.username)
