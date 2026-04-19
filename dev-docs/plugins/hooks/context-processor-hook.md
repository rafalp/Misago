# `context_processor_hook`

This hook allows plugin authors to inject custom data into the template context without creating a custom context processor.


## Location

This hook can be imported from `misago.context_processors.hooks`:

```python
from misago.context_processors.hooks import context_processor_hook
```


## Filter

```python
def custom_context_processor_filter(
    action: ContextProcessorHookAction, request: HttpRequest
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ContextProcessorHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `state: ThreadStartState`

A `ThreadStartState` instance containing data used to create a new thread.


### Return value

`True` if the new thread should require moderator approval, or `False` otherwise.


## Action

```python
def context_processor_action(request: HttpRequest) -> dict:
    ...
```

A standard function that Misago uses to check if a new thread should require moderator approval.


### Arguments

#### `state: ThreadStartState`

A `ThreadStartState` instance containing data used to create a new thread.


### Return value

`dict` with context data.


## Example: inject extra data into a template context

```python
from django.http import HttpRequest
from misago.context_processors.hooks import context_processor_hook


@context_processor_hook.append_filter
def plugin_context_data(
    action, request: HttpRequest
) -> dict:
    context_data = action(request)

    context_data["my_plugin_data"] = request.my_plugin_data

    return context_data
```


## Example: include template components in the base template

```python
from django.http import HttpRequest
from misago.context_processors.hooks import context_processor_hook


@context_processor_hook.append_filter
def plugin_context_data(
    action, request: HttpRequest
) -> dict:
    context_data = action(request)

    if not request.session.get("cookie_agreement"):
        # Only `template_name` key is required,
        # other keys will be merged with included template's context
        context_data["below_footer"].append(
            {
                "template_name": "cookie_agreement.html",
                "agreement_message:": request.settings.cookie_agreement,
            }
        )

    return context_data
```