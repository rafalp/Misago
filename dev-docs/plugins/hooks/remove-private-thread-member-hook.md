# `remove_private_thread_member_hook`

This hook allows plugins to replace or extend the logic for removing a member from a private thread.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import remove_private_thread_member_hook
```


## Filter_This section is empty._


## Action_This section is empty._


## Example

Record the IP address used to remove a member from a thread:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import remove_private_thread_member_hook
from misago.threads.models import Thread
from misago.threadupdates.models import ThreadUpdate
from misago.users.models import User


@remove_private_thread_member_hook.append_filter
def record_private_thread_remove_member_actor_ip(
    action,
    actor: User | str | None,
    thread: Thread,
    member: User,
    request: HttpRequest | None = None,
) -> ThreadUpdate:
    thread_update = action(actor, thread, member, request)

    thread_update.plugin_data["user_ip"] = request.user_ip
    thread_update.save(update_fields=["plugin_data"])

    return thread_update
```