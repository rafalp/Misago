# `get_start_private_thread_formset_hook`

This hook wraps the standard function that Misago uses to create a new `StartPrivateThreadFormset` instance with forms for posting a new private thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_start_private_thread_formset_hook
```


## Filter

```python
def custom_get_start_private_thread_formset_filter(
    action: GetStartPrivateThreadFormsetHookAction,
    request: HttpRequest,
    category: Category,
) -> 'StartPrivateThreadFormset':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetStartPrivateThreadFormsetHookAction`

A standard function that Misago uses to create a new `StartPrivateThreadFormset` instance with forms for posting a new private thread.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `StartPrivateThreadFormset` instance with forms for posting a new private thread.


## Action

```python
def get_start_private_thread_formset_action(request: HttpRequest, category: Category) -> 'StartPrivateThreadFormset':
    ...
```

A standard function that Misago uses to create a new `StartPrivateThreadFormset` instance with forms for posting a new private thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `StartPrivateThreadFormset` instance with forms for posting a new private thread.


## Example

The code below implements a custom filter function that adds custom form to the start new private thread formset:

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.posting.formsets import StartPrivateThreadFormset
from misago.posting.hooks import get_start_private_thread_formset_hook

from .forms import SelectUserForm


@get_start_private_thread_formset_hook.append_filter
def add_select_user_form(
    action, request: HttpRequest, category: Category
) -> StartPrivateThreadFormset:
    formset = action(request, category)

    if request.method == "POST":
        form = SelectUserForm(request.POST, prefix="select-user")
    else:
        form = SelectUserForm(prefix="select-user")

    formset.add_form(form, before="posting=title")
    return formset
```