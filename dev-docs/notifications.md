# Notifications reference

Misago's notifications feature is implemented in the `misago.notifications` package.


## Notification model

In Misago notifications are represented as instances of `misago.notifications.models.Notification` Django model.

This model has following fields:

- `id`: an `int` with primary key.
- `user`: an foreign key to `misago.users.models.User`.
- `verb`: a `str` with this notification's type. Max 32 characters.
- `is_read`: a `bool` marking this notification as read or unread. Defaults to `False` (unread).
- `actor`: an foreign key to `misago.users.models.User`, nullable.
- `actor_name`: a `str` with actor username, nullable. Max 255 characters.
- `category`: an foreign key to `misago.categories.models.Category`, nullable.
- `thread`: an foreign key to `misago.threads.models.Thread`, nullable.
- `thread_title`: a `str` with thread title, nullable. Max 255 characters.
- `post`: an foreign key to `misago.threads.models.Post`, nullable.
- `created_at`: `datetime` of notification's creation.


## Notifying users

To notify user about an event, use `notify_user` function from `misago.notifications.users`:

```python
def notify_user(
    user: "User",
    verb: str,
    actor: Optional["User"] = None,
    category: Optional[Category] = None,
    thread: Optional[Thread] = None,
    post: Optional[Post] = None,
) -> Notification:
    ...
```

This function performs two tasks:

- It saves new `misago.notifications.models.Notification` instance to database.
- It increases `user.unread_notifications` counter in database.

It takes two required arguments:

- `user`: an instance of `misago.users.models.User` representing user to notify.
- `verb`: a `str` with notification's "verb", eg. `REPLIED`, `FOLLOWED`.

It takes four optional arguments:

- `actor`: an instance of `misago.users.models.User` representing the user who caused the event.
- `category`: an instance of `misago.categories.models.Categry` representing category in which the event has occurred.
- `thread`: an instance of `misago.threads.models.Thread` representing thread in which the event has occurred.
- `post`: an instance of `misago.threads.models.Post` representing post in which the event has occurred.

Example `notify_user` call executed by Misago to notify an user watching a thread about new reply looks like this:

```python
notify_user(
    watched_thread.user,
    "REPLIED",
    actor=reply.poster,
    category=reply.category,
    thread=reply.thread,
    post=reply,
) 
```


## Adding custom notifications

Misago supports adding custom notifications for new events by plugins.


### Notification verb

Each notification type is a "verb", a `str` representing the action (or event) that caused this notification.

Standard verbs used by Misago are defined on `misago.notifications.verbs.NotificationVerb` enumerable.

There's also special `TEST` verb thats not defined on `NotificationVerb` but is still supported for testing purposes.

Custom verbs can be any Python string not longer than 32 characters. To reduce the risk of your custom verb conflicting with other plugin or future Misago release I recommend prefixing it with name of your plugin, eg. `USER_VOTES_VOTED`.

Once you've decided on verb for your notification, you will be able to implement message and redirect url for it.


### Notification registry

Misago uses factory functions to retrieve notifications messages and redirect urls.

Those factory functions are registered in special registry, importable as `registry` from `misago.notifications.registry` module.


### Notification message

Factory function for notification's message is called with single argument, `Notification` instance, and returns **escaped** `str` with HTML for notification message:

```python
def get_verb_notification_message(notification: Notification) -> str:
    return html.escape(f"Test notification #{notification.id}")
```

> **Note:** For performance reasons foreign key fields on `Notification` model are not populated when notifications list is retrieved.
> 
> Use `notification.actor_name` field to retrieve actor's name and `notification.thread_title` field to retrieve thread's title.

To register custom function as message factory for verb, use `registry`'s `message` method:

```python
import html

from misago.notifications.registry import Notification, registry


# `message` works as a decorator
@registry.message("CUSTOM")
def get_custom_notification_message(notification: Notification) -> str:
    return html.escape(f"Custom notification in {notification.thread_title}")


# `message` can also be used as a setter
def get_custom_notification_message(notification: Notification) -> str:
    return html.escape(f"Custom notification in {notification.thread_title}")


registry.message("CUSTOM", get_custom_notification_message)
```


### Notification redirect url

Factory function for notification's redirect url is called with two arguments, Django's `HttpRequest` instance and the `Notification` instance, and retuurns `str` with URL to which user should be redirected to see notification's source:

```python
def get_verb_notification_redirect_url(request: HttpRequest, notification: Notification) -> str:
    return reverse(
        "my-plugin:some-url",
        kwargs={
            "id": notification.thread.id,
            "slug": notification.thread.slug,
        },
    )
```

> **Note:** Foreign key fields on `Notification` model are populated with related objects when notification redirect url is retrieved.


To register custom function as redirect url factory for verb, use `registry`'s `redirect` method:

```python
from django.http import HttpRequest
from django.urls import reverse
from misago.notifications.registry import Notification, registry


# `redirect` works as a decorator
@registry.redirect("CUSTOM")
def get_custom_notification_redirect_url(
    request: HttpRequest, notification: Notification
) -> str:
    return reverse(
        "my-plugin:some-url",
        kwargs={
            "id": notification.thread.id,
            "slug": notification.thread.slug,
        },
    )


# `redirect` can also be used as a setter
def get_custom_notification_redirect_url(
    request: HttpRequest, notification: Notification
) -> str:
    return reverse(
        "my-plugin:some-url",
        kwargs={
            "id": notification.thread.id,
            "slug": notification.thread.slug,
        },
    )


registry.redirect("CUSTOM", get_custom_notification_redirect_url)
```


## Unsupported notification verbs

It is possible for a notification to have a verb that is not recognized by Misago. Such a notification may have been created by a plugin that is no longer installed or that was changed to no longer support it.

When this happens, Misago will produce a fallback notification message using the `{actor} {verb} {thread_title}` scheme. It will also display the "page not found" error when the user clicks on the notification.
