from typing import TYPE_CHECKING, Callable, Dict, overload

from .exceptions import NotificationVerbError

if TYPE_CHECKING:
    from .models import Notification


MessageCallable = Callable[["Notification"], str]


class NotificationMessageFactory:
    _verbs: Dict[str, MessageCallable]

    def __init__(self):
        self._verbs = {}

    @overload
    def set_message(self, verb: str) -> Callable[[MessageCallable], MessageCallable]:
        ...

    def set_message(self, verb: str, factory: MessageCallable | None = None) -> None:
        """Register `factory` function as message factory.

        Can be called with two arguments or used as decorator:

        ```python
        message_factory.set_message("replied", get_replied_message)

        # ...or...

        @message_factory.set_message("replied")
        def get_replied_message(notification: Notification) -> str:
            ...
        ```
        """
        if factory:
            self._verbs[verb] = factory
            return

        def register_factory(f: MessageCallable):
            self._verbs[verb] = f
            return f

        return register_factory

    def get_message(self, notification: "Notification") -> str:
        """Returns `str` with message for given notification.

        Raises `NotificationVerbError` when there's no message function for
        given notification type.

        ```python
        message = message_factory.get_message(notification)
        ```
        """
        try:
            return self._verbs[notification.verb](notification)
        except KeyError as exc:
            raise NotificationVerbError(notification.verb) from exc


message_factory = NotificationMessageFactory()


@message_factory.set_message("test")
def get_test_notification_message(notification: "Notification") -> str:
    return f"Test notification #{notification.id}"
