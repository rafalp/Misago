# Notifications guide

Misago's notifications feature is implemented in `misago.notifications` package.


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
- It increases `user.unread_notifications` attribute in database.

It takes two required arguments:

- `user`: an instance of `misago.users.models.User` representing user to notify.
- `verb`: a `str` with notification's "verb", eg. `REPLIED`, `FOLLOWED`.

It optionally takes following arguments:

- `actor`: an instance of `misago.users.models.User` representing user who caused the event.
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


## Adding custom notification

Misago supports adding custom notifications for new events.


### Notification verb

Each notification type is a "verb", a `str` representing the action (or event) that caused this notification.

Standard verbs used by Misago are defined on `misago.notifications.verbs.NotificationVerb` enumerable.

There's also special `TEST` verb thats not defined on `NotificationVerb` but is still supported for testing purposes.

Custom verbs can be any Python string not longer than 32 characters. To reduce the risk of your custom verb conflicting with other plugin or future Misago release I recommend prefixing it with name of your plugin, eg. `USER_VOTES_VOTED`.

Once you've decided on verb for your notification, you will be able to implement message and redirect url for it.


### Notification message

Notification messages are not stored in the database. Instead they are created dynamically by a function associated with given `verb` from `Notification` instances.

Function used to retrieve notification's message looks like this:

```python
def get_verb_notification_message(notification: Notification) -> str:
    return f"Test notification #{notification.id}"
```

> **Note:** For performance reasons foreign key fields on `Notification` model are not populated when notifications list is retrieved.
> 
> Use `notification.actor_name` field to retrieve actor's name and `notification.thread_title` field to retrieve thread's title.

To know which function to use for the verb, Misago uses instance of `misago.notifications.messages.NotificationMessageFactory` class, importable as `message_factory` from same package.

This instance implements the `set_message` method which can be used to set notification's message factory for given verb:

```python
from misago.notifications.messages import Notification, message_factory

# Use `set_message` as decorator
@message_factory.set_message("CUSTOM")
def get_custom_notification_message(notification: Notification) -> str:
    return f"Custom notification in {notification.thread_title}"


# Or as setter
def get_custom_notification_message(notification: Notification) -> str:
    return f"Custom notification in {notification.thread_title}"


message_factory.set_message("CUSTOM", get_custom_notification_message)
```


### Notification redirect url

Notification urls are created dynamically by a function associated with given `verb` from `HttpRequest` and `Notification` instances.

Function used to retrieve notification's redirect url looks like this:

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

To know which function to use for the verb, Misago uses instance of `misago.notifications.redirects.NotificationRedirectFactory` class, importable as `redirect_factory` from same package.

This instance implements the `set_redirect` method which can be used to set notification's redirect url factory for given verb:

```python
from django.http import HttpRequest
from django.urls import reverse
from misago.notifications.redirects import Notification, redirect_factory

# Use `set_message` as decorator
@redirect_factory.set_message("CUSTOM")
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


# Or as setter
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


redirect_factory.set_message("CUSTOM", get_custom_notification_redirect_url)
```