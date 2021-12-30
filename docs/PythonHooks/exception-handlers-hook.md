# `exception_handlers_hook`

```python
exception_handlers_hook.call_action(
    action: ExceptionHandlersAction,
)
```

A synchronous filter for the function used to create exception handlers for ASGI app.

Returns [dict of exception handlers](https://www.starlette.io/exceptions/#errors-and-handled-exceptions) for Starlette, eg:

```python
return {
    404: not_found,
    500: server_error,
}
```


## Required arguments

### `action`

```python
async def exception_handlers():
    ...
```

Next filter or built-in function used to retrieve exception handlers.
