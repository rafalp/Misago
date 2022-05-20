# `graphql_context_hook`

```python
from misago.graphql.hooks import graphql_context_hook

graphql_context_hook.call_action(action: ContextAction, request: Request)
```

A filter for the function used to create a GraphQL context.

Returns `Context` dict with current GraphQL query context.


## Required arguments

### `action`

```python
async def get_graphql_context(request: Request) -> Context:
    ...
```

Next filter or built-in function used to create GraphQL context.


## `request`

```python
Request
```

An instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to GraphQL API.