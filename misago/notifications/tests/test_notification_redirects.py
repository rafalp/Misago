import pytest

from ..exceptions import NotificationVerbError
from ..models import Notification
from ..redirects import NotificationRedirectFactory, redirect_factory


@pytest.fixture
def request_mock(rf, user):
    request = rf.get("/notification/1/")

    request.user = user

    return request


def test_notification_redirect_factory_can_have_redirect_set_with_setter(request_mock):
    factory = NotificationRedirectFactory()
    factory.set_redirect("TEST", lambda _, obj: f"/test/#{obj.id}")

    redirect = factory.get_redirect_url(request_mock, Notification(id=1, verb="TEST"))
    assert redirect == "/test/#1"


def test_notification_redirect_factory_can_have_redirect_set_with_decorator(
    request_mock,
):
    factory = NotificationRedirectFactory()

    @factory.set_redirect("TEST")
    def get_test_redirect_url(request, obj):
        return f"/test/#{obj.id}"

    redirect = factory.get_redirect_url(request_mock, Notification(id=1, verb="TEST"))
    assert redirect == "/test/#1"


def test_notification_redirect_factory_raises_verb_error_for_unknown_verb(request_mock):
    factory = NotificationRedirectFactory()

    with pytest.raises(NotificationVerbError) as excinfo:
        factory.get_redirect_url(request_mock, Notification(id=1, verb="TEST"))

    assert "TEST" in str(excinfo)


def test_default_redirect_factory_supports_test_notifications(request_mock):
    redirect = redirect_factory.get_redirect_url(
        request_mock, Notification(id=1, verb="TEST")
    )
    assert redirect == "/#test-notification-1"
