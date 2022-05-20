# `template_context_hook`

```python
from misago.template.hooks import template_context_hook

template_context_hook.call_action(action: TemplateContextAction, request: Request)
```

A filter for the function used to create default template context.

Returns `TemplateContext` dict with default template context.


## Required arguments

### `action`

```python
async def get_default_context(request: Request) -> TemplateContext:
    ...
```

Next filter or built-in function used to create a template context.


## `request`

```python
Request
```

An instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to application.