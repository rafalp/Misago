from datetime import timedelta

import pytest
from django.utils import timezone

from ..audittrail import create_audit_trail, create_user_audit_trail
from ..models import AuditTrail
from ..signals import remove_old_ips

USER_IP = "13.41.51.41"


class RequestMock:
    user_ip = USER_IP

    def __init__(self, user):
        self.user = user


@pytest.fixture
def request_mock(user):
    return RequestMock(user)


def test_audit_trail_creation_raises_value_error_if_target_is_not_model_instance(
    request_mock, anonymous_user
):
    with pytest.raises(ValueError):
        create_audit_trail(request_mock, anonymous_user)


def test_audit_trail_is_not_created_for_anonymous_users(anonymous_user, user):
    request_mock = RequestMock(anonymous_user)
    create_audit_trail(request_mock, user)
    assert not AuditTrail.objects.exists()


def test_audit_trail_is_created(request_mock, other_user):
    assert create_audit_trail(request_mock, other_user)
    assert AuditTrail.objects.exists()


def test_audit_trail_is_created_with_request_data(request_mock, user, other_user):
    audit_trail = create_audit_trail(request_mock, other_user)

    assert audit_trail.user == user
    assert audit_trail.ip_address == USER_IP


def test_audit_trail_is_created_with_generic_relation_to_target(
    request_mock, user, other_user
):
    audit_trail = create_audit_trail(request_mock, other_user)
    assert audit_trail.content_object == other_user


def test_audit_trail_is_deleted_together_with_user(request_mock, user, other_user):
    audit_trail = create_audit_trail(request_mock, other_user)
    user.delete(anonymous_username="Deleted")
    with pytest.raises(AuditTrail.DoesNotExist):
        audit_trail.refresh_from_db()


def test_audit_trail_is_kept_after_its_target_is_deleted(request_mock, other_user):
    audit_trail = create_audit_trail(request_mock, other_user)
    other_user.delete(anonymous_username="Deleted")
    audit_trail.refresh_from_db()


def test_deleting_audit_trail_leaves_user(request_mock, user, other_user):
    audit_trail = create_audit_trail(request_mock, other_user)
    audit_trail.delete()
    user.refresh_from_db()


def test_deleting_audit_trail_leaves_target(request_mock, user, other_user):
    audit_trail = create_audit_trail(request_mock, other_user)
    audit_trail.delete()
    other_user.refresh_from_db()


def test_audit_trail_can_be_created_without_request(user, other_user):
    assert create_user_audit_trail(user, USER_IP, other_user)
    assert AuditTrail.objects.exists()


def test_audit_trail_creation_without_request_raises_value_error_if_target_is_not_model(
    user, anonymous_user
):
    with pytest.raises(ValueError):
        create_user_audit_trail(user, USER_IP, anonymous_user)


def test_audit_trail_without_request_is_created_with_explicit_data(user, other_user):
    audit_trail = create_user_audit_trail(user, USER_IP, other_user)

    assert audit_trail.user == user
    assert audit_trail.ip_address == USER_IP


def test_audit_trail_without_request_is_created_with_generic_relation_to_target(
    user, other_user
):
    audit_trail = create_user_audit_trail(user, USER_IP, other_user)
    assert audit_trail.content_object == other_user


def test_recent_audit_trail_is_not_deleted_on_signal(user, other_user):
    create_user_audit_trail(user, USER_IP, other_user)
    remove_old_ips.send(None, ip_storage_time=1)
    assert user.audittrail_set.exists()


def test_old_audit_trail_is_deleted_on_signal(user, other_user):
    audit_trail = create_user_audit_trail(user, USER_IP, other_user)
    audit_trail.created_on = timezone.now() - timedelta(days=6)
    audit_trail.save()

    remove_old_ips.send(None, ip_storage_time=5)
    assert not user.audittrail_set.exists()
