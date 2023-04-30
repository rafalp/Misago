from typing import TYPE_CHECKING, Callable, Dict, overload

from .exceptions import NotificationVerbError

if TYPE_CHECKING:
    from .models import Notification


RedirectCallable = Callable[["Notification"], str]


class NotificationRedirectFactory:
    _verbs: Dict[str, RedirectCallable]

    def __init__(self):
        self._verbs = {}

    @overload
    def set_redirect(self, verb: str) -> Callable[[RedirectCallable], RedirectCallable]:
        ...

    def set_redirect(self, verb: str, factory: RedirectCallable | None = None) -> None:
        """Register `factory` function as redirect url factory.

        Can be called with two arguments or used as decorator:

        ```python
        redirect_factory.set_redirect("replied", get_replied_post_url)

        # ...or...

        @redirect_factory.set_redirect("replied")
        def get_replied_post_url(notification: Notification) -> str:
            ...
        ```
        """
        if factory:
            self._verbs[verb] = factory
            return

        def register_factory(f: RedirectCallable):
            self._verbs[verb] = f
            return f

        return register_factory

    def get_redirect_url(self, notification: "Notification") -> str:
        """Returns `str` with redirect url to given notification's target.

        Raises `NotificationVerbError` when there's no redirect function for
        given notification type.

        ```python
        message = redirect_factory.get_redirect_url(notification)
        ```
        """
        try:
            return self._verbs[notification.verb](notification)
        except KeyError as exc:
            raise NotificationVerbError(notification.verb) from exc


redirect_factory = NotificationRedirectFactory()


@redirect_factory.set_redirect("TEST")
def get_test_notification_url(notification: "Notification") -> str:
    return f"/#test-notification-{notification.id}"
