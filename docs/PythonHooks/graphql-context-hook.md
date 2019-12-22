# `graphql_context_hook`

```python
graphql_context_hook.call_action(action: GraphQLContextAction, request: Request)
```

A filter for the function used to create a GraphQL context.

Returns `GraphQLContext` dict with current GraphQL query context.


## Required arguments

### `action`

```python
async def get_graphql_context(request: Request) -> GraphQLContext:
    ...
```

Next filter or built-in function used to create GraphQL context.


## `request`

```python
Request
```

An instance of [`Request`](https://www.starlette.io/requests/) representing current HTTP request to GraphQL API.