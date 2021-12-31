# `register_routes_hook`

```python
from misago.routes.hooks import register_routes_hook

register_routes_hook.call_action(
    action: RegisterRoutesAction,
    app: Starlette,
)
```

A synchronous filter for the function used to register routes in ASGI app.

Returns nothing.


## Required arguments

### `action`

```python
async def register_routes(app: Starlette):
    ...
```

Next filter or built-in function used to register routes in ASGI app.
