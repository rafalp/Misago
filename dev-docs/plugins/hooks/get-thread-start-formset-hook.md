# `get_thread_start_formset_hook`

This hook wraps the standard function that Misago uses to create a new `ThreadStartFormset` instance with forms for starting a new thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_thread_start_formset_hook
```


## Filter

```python
def custom_get_thread_start_formset_filter(
    action: GetThreadStartFormsetHookAction,
    request: HttpRequest,
    category: Category,
) -> 'ThreadStartFormset':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadStartFormsetHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `ThreadStartFormset` instance with forms for posting a new thread.


## Action

```python
def get_thread_start_formset_action(request: HttpRequest, category: Category) -> 'ThreadStartFormset':
    ...
```

A standard function that Misago uses to create a new `ThreadStartFormset` instance with forms for starting a new thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `ThreadStartFormset` instance with forms for posting a new thread.


## Example

The code below implements a custom filter function that adds custom form to the start new thread formset:

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.posting.formsets import ThreadStartFormset
from misago.posting.hooks import get_thread_start_formset_hook

from .forms import SelectUserForm


@get_thread_start_formset_hook.append_filter
def add_select_user_form(
    action, request: HttpRequest, category: Category
) -> ThreadStartFormset:
    formset = action(request, category)

    if request.method == "POST":
        form = SelectUserForm(request.POST, prefix="select-user")
    else:
        form = SelectUserForm(prefix="select-user")

    formset.add_form(form, before="posting-title")
    return formset
```