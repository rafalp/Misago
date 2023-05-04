import pytest

from ..exceptions import NotificationVerbError
from ..messages import NotificationMessageFactory, message_factory
from ..models import Notification
from ..verbs import NotificationVerb


def test_notification_message_factory_can_have_message_set_with_setter():
    factory = NotificationMessageFactory()
    factory.set_message("TEST", lambda obj: f"Hello #{obj.id}")

    message = factory.get_message(Notification(id=1, verb="TEST"))
    assert message == "Hello #1"


def test_notification_message_factory_can_have_message_set_with_decorator():
    factory = NotificationMessageFactory()

    @factory.set_message("TEST")
    def get_test_message(obj):
        return f"Hello #{obj.id}"

    message = factory.get_message(Notification(id=1, verb="TEST"))
    assert message == "Hello #1"


def test_notification_message_factory_raises_verb_error_for_unknown_verb():
    factory = NotificationMessageFactory()

    with pytest.raises(NotificationVerbError) as excinfo:
        factory.get_message(Notification(id=1, verb="TEST"))

    assert "TEST" in str(excinfo)


def test_default_message_factory_supports_test_notifications():
    message = message_factory.get_message(Notification(id=1, verb="TEST"))
    assert message == "Test notification #1"


def test_default_message_factory_supports_replies_notifications():
    message = message_factory.get_message(
        Notification(
            id=1,
            verb=NotificationVerb.REPLIED,
            actor_name="Aerith",
            thread_title="Midgar was destroyed!",
        )
    )
    assert message == (
        "<b>Aerith</b> replied to the thread <b>Midgar was destroyed!</b>."
    )