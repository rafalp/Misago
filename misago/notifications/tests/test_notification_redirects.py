import pytest

from ..exceptions import NotificationVerbError
from ..redirects import NotificationRedirectFactory, redirect_factory
from ..models import Notification


def test_notification_redirect_factory_can_have_redirect_set_with_setter():
    factory = NotificationRedirectFactory()
    factory.set_redirect("test", lambda obj: f"/test/#{obj.id}")

    redirect = factory.get_redirect_url(Notification(id=1, verb="test"))
    assert redirect == "/test/#1"


def test_notification_redirect_factory_can_have_redirect_set_with_decorator():
    factory = NotificationRedirectFactory()

    @factory.set_redirect("test")
    def get_test_redirect_url(obj):
        return f"/test/#{obj.id}"

    redirect = factory.get_redirect_url(Notification(id=1, verb="test"))
    assert redirect == "/test/#1"


def test_notification_redirect_factory_raises_verb_error_for_unknown_verb():
    factory = NotificationRedirectFactory()

    with pytest.raises(NotificationVerbError) as excinfo:
        factory.get_redirect_url(Notification(id=1, verb="test"))

    assert "test" in str(excinfo)


def test_default_redirect_factory_supports_test_notifications():
    redirect = redirect_factory.get_redirect_url(Notification(id=1, verb="test"))
    assert redirect == f"/#test-notification-1"
