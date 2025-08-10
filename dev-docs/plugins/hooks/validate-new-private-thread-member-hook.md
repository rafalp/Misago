# `validate_new_private_thread_member_hook`

This hook allows plugins to replace or extend the standard logic for validating new private thread members.


## Location

This hook can be imported from `misago.privatethreadmembers.hooks`:

```python
from misago.privatethreadmembers.hooks import validate_new_private_thread_member_hook
```


## Filter

```python
def custom_validate_new_private_thread_member_filter(
    action: ValidateNewPrivateThreadMemberHookAction,
    new_member_permissions: 'UserPermissionsProxy',
    other_user_permissions: 'UserPermissionsProxy',
    cache_versions: dict,
    request: HttpRequest | None=None,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ValidateNewPrivateThreadMemberHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `new_member_permissions: UserPermissionsProxy`

A proxy object with the invited user's permissions.


#### `other_user_permissions: UserPermissionsProxy`

A proxy object with the inviting user's permissions.


#### `cache_versions: dict`

A Python `dict` with cache versions.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def validate_new_private_thread_member_action(
    new_member_permissions: 'UserPermissionsProxy',
    other_user_permissions: 'UserPermissionsProxy',
    cache_versions: dict,
    request: HttpRequest | None=None,
):
    ...
```

Misago function for validating new private thread members.


### Arguments

#### `new_member_permissions: UserPermissionsProxy`

A proxy object with the invited user's permissions.


#### `other_user_permissions: UserPermissionsProxy`

A proxy object with the inviting user's permissions.


#### `cache_versions: dict`

A Python `dict` with cache versions.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Block new users from inviting non-staff users to their private threads.

```python
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils import timezone
from misago.permissions.proxy import UserPermissionsProxy
from misago.privatethreadmembers.hooks import validate_new_private_thread_member_hook


@validate_new_private_thread_member_hook.append_filter
def validate_new_private_thread_member_registration_date(
    action,
    new_member_permissions: UserPermissionsProxy,
    other_user_permissions: UserPermissionsProxy,
    cache_versions: dict,
    request: HttpRequest | None = None,
):
    action(
        new_member_permissions,
        other_user_permissions,
        cache_versions,
        request,
    )

    user_is_new = (timezone.now() - user.joined_on).days < 7

    if user_is_new and not new_member_permissions.moderated_categories:
        raise ValidationError(
            "Your account is less than 7 days old."
        )
```