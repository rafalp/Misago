import pytest

from ..exceptions import NotificationVerbError
from ..registry import NotificationRegistry, registry
from ..models import Notification
from ..verbs import NotificationVerb


@pytest.fixture
def request_mock(rf, user):
    request = rf.get("/notification/1/")

    request.user = user

    return request


def test_notification_registry_can_have_message_set_with_setter():
    notification_registry = NotificationRegistry()
    notification_registry.message("TEST", lambda obj: f"Hello #{obj.id}")

    message = notification_registry.get_message(Notification(id=1, verb="TEST"))
    assert message == "Hello #1"


def test_notification_registry_can_have_message_set_with_decorator():
    notification_registry = NotificationRegistry()

    @notification_registry.message("TEST")
    def get_test_message(obj):
        return f"Hello #{obj.id}"

    message = notification_registry.get_message(Notification(id=1, verb="TEST"))
    assert message == "Hello #1"


def test_notification_registry_get_message_produces_message_for_unsupported_verb():
    notification_registry = NotificationRegistry()

    message = notification_registry.get_message(Notification(id=1, verb="REMOVED"))
    assert message == "REMOVED"


def test_notification_registry_get_message_produces_message_with_actor_name_for_unsupported_verb():
    notification_registry = NotificationRegistry()

    message = notification_registry.get_message(
        Notification(id=1, verb="REMOVED", actor_name="ACTOR")
    )
    assert message == "<b>ACTOR</b> REMOVED"


def test_notification_registry_get_message_produces_message_with_thread_title_for_unsupported_verb():
    notification_registry = NotificationRegistry()

    message = notification_registry.get_message(
        Notification(id=1, verb="REMOVED", thread_title="THREAD")
    )
    assert message == "REMOVED <b>THREAD</b>"


def test_notification_registry_get_message_produces_message_with_actor_and_thread_for_unsupported_verb():
    notification_registry = NotificationRegistry()

    message = notification_registry.get_message(
        Notification(
            id=1,
            verb="REMOVED",
            actor_name="ACTOR",
            thread_title="THREAD",
        )
    )
    assert message == "<b>ACTOR</b> REMOVED <b>THREAD</b>"


def test_notification_registry_can_have_redirect_set_with_setter(request_mock):
    notification_registry = NotificationRegistry()
    notification_registry.redirect("TEST", lambda _, obj: f"/test/#{obj.id}")

    redirect = notification_registry.get_redirect_url(
        request_mock, Notification(id=1, verb="TEST")
    )
    assert redirect == "/test/#1"


def test_notification_registry_can_have_redirect_set_with_decorator(
    request_mock,
):
    notification_registry = NotificationRegistry()

    @notification_registry.redirect("TEST")
    def get_test_redirect_url(request, obj):
        return f"/test/#{obj.id}"

    redirect = notification_registry.get_redirect_url(
        request_mock, Notification(id=1, verb="TEST")
    )
    assert redirect == "/test/#1"


def test_notification_registry_get_redirect_url_raises_verb_error_for_unknown_verb(
    request_mock,
):
    notification_registry = NotificationRegistry()

    with pytest.raises(NotificationVerbError) as excinfo:
        notification_registry.get_redirect_url(
            request_mock, Notification(id=1, verb="TEST")
        )

    assert "TEST" in str(excinfo)


def test_default_notification_registry_supports_test_notifications(request_mock):
    message = registry.get_message(Notification(id=1, verb="TEST"))
    assert message == "Test notification #1"

    redirect = registry.get_redirect_url(request_mock, Notification(id=1, verb="TEST"))
    assert redirect == "/#test-notification-1"


def test_default_notification_registry_supports_reply_notifications():
    message = registry.get_message(
        Notification(
            id=1,
            verb=NotificationVerb.REPLIED,
            actor_name="Aerith",
            thread_title="Midgar was destroyed!",
        )
    )
    assert message == ("<b>Aerith</b> replied to <b>Midgar was destroyed!</b>")


def test_default_notification_registry_supports_invite_notifications():
    message = registry.get_message(
        Notification(
            id=1,
            verb=NotificationVerb.INVITED,
            actor_name="Aerith",
            thread_title="Midgar was destroyed!",
        )
    )
    assert message == ("<b>Aerith</b> invited you to <b>Midgar was destroyed!</b>")
