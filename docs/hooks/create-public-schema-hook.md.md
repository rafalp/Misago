# `create_public_schema_hook`

```python
from ariadne_graphql_modules import BaseType
from misago.graphql.hooks import create_public_schema_hook

create_public_schema_hook.call_action(
    action: CreatePublicSchemaAction, *types: BaseType
)
```

A filter for the function used to create GraphQL schema used by public API.

Returns `GraphQLSchema` instance as defined by `graphql` library.


## Required arguments

### `action`

```python
async def create_schema_hook(*types: BaseType) -> GraphQLSchema:
    ...
```

Next filter or built-in function used to create GraphQL schema.
