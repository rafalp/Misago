import html
from typing import TYPE_CHECKING, Callable, Dict, overload

from django.http import HttpRequest
from django.utils.translation import pgettext

from ..threads.views.redirect import get_redirect_to_post_response
from .verbs import NotificationVerb
from .exceptions import NotificationVerbError

if TYPE_CHECKING:
    from .models import Notification


MessageFactory = Callable[["Notification"], str]
RedirectFactory = Callable[["HttpRequest", "Notification"], str]


class NotificationRegistry:
    _messages: Dict[str, MessageFactory]
    _redirects: Dict[str, RedirectFactory]

    def __init__(self):
        self._messages = {}
        self._redirects = {}

    @overload
    def message(self, verb: str) -> Callable[[MessageFactory], MessageFactory]: ...

    def message(self, verb: str, factory: MessageFactory | None = None) -> None:
        """Register `factory` function as message factory.

        Can be called with two arguments or used as decorator:

        ```python
        registry.message("replied", get_replied_message)

        # ...or...

        @registry.message("replied")
        def get_replied_message(notification: Notification) -> str:
            ...
        ```
        """
        if factory:
            self._messages[verb] = factory
            return

        def register_factory(f: MessageFactory):
            self._messages[verb] = f
            return f

        return register_factory

    def get_message(self, notification: "Notification") -> str:
        """Returns `str` with message for given notification.

        Raises `NotificationVerbError` when there's no message function for
        given notification type.

        ```python
        message = registry.get_message(notification)
        ```
        """
        try:
            return self._messages[notification.verb](notification)
        except KeyError:
            return get_unsupported_verb_notification_message(notification)

    @overload
    def redirect(self, verb: str) -> Callable[[RedirectFactory], RedirectFactory]: ...

    def redirect(self, verb: str, factory: RedirectFactory | None = None) -> None:
        """Register `factory` function as redirect url factory.

        Can be called with two arguments or used as decorator:

        ```python
        registry.redirect("replied", get_replied_post_url)

        # ...or...

        @registry.redirect("replied")
        def get_replied_post_url(notification: Notification) -> str:
            ...
        ```
        """
        if factory:
            self._redirects[verb] = factory
            return

        def register_factory(f: RedirectFactory):
            self._redirects[verb] = f
            return f

        return register_factory

    def get_redirect_url(
        self, request: HttpRequest, notification: "Notification"
    ) -> str:
        """Returns `str` with redirect url to given notification's target.

        Raises `NotificationVerbError` when there's no redirect function for
        given notification type.

        ```python
        message = registry.get_redirect_url(request, notification)
        ```
        """
        try:
            return self._redirects[notification.verb](request, notification)
        except KeyError as exc:
            raise NotificationVerbError(notification.verb) from exc


registry = NotificationRegistry()


# Fallback: used to produce messages for unsupported verbs
def get_unsupported_verb_notification_message(notification: "Notification") -> str:
    message = notification.verb

    if notification.actor_name:
        message = f"{bold_escape(notification.actor_name)} {message}"
    if notification.thread_title:
        message = f"{message} {bold_escape(notification.thread_title)}"

    return message


# TEST: used in tests only


@registry.message("TEST")
def get_test_notification_message(notification: "Notification") -> str:
    return f"Test notification #{notification.id}"


@registry.redirect("TEST")
def get_test_notification_url(
    request: HttpRequest, notification: "Notification"
) -> str:
    return f"/#test-notification-{notification.id}"


# REPLIED: new reply in thread or private thread


@registry.message(NotificationVerb.REPLIED)
def get_replied_notification_message(notification: "Notification") -> str:
    message = html.escape(
        pgettext("notification replied", "%(actor)s replied to %(thread)s")
    )
    return message % {
        "actor": bold_escape(notification.actor_name),
        "thread": bold_escape(notification.thread_title),
    }


@registry.redirect(NotificationVerb.REPLIED)
def get_replied_notification_url(
    request: HttpRequest, notification: "Notification"
) -> str:
    post = notification.post
    post.category = notification.category

    response = get_redirect_to_post_response(request, post)

    return response.headers["location"]


# INVITED: invited to private thread


@registry.message(NotificationVerb.INVITED)
def get_invited_notification_message(notification: "Notification") -> str:
    message = html.escape(
        pgettext("notification invited", "%(actor)s invited you to %(thread)s")
    )
    return message % {
        "actor": bold_escape(notification.actor_name),
        "thread": bold_escape(notification.thread_title),
    }


@registry.redirect(NotificationVerb.INVITED)
def get_invited_notification_url(
    request: HttpRequest, notification: "Notification"
) -> str:
    return notification.category.thread_type.get_thread_absolute_url(
        notification.thread
    )


def bold_escape(value: str) -> str:
    return f"<b>{html.escape(value)}</b>"
