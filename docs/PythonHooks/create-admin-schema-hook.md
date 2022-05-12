# `create_admin_schema_hook`

```python
from ariadne_graphql_modules import BaseType
from misago.graphql.hooks import create_admin_schema_hook

create_admin_schema_hook.call_action(
    action: CreateAdminSchemaAction, *types: BaseType
)
```

A filter for the function used to create GraphQL schema used by admin API.

Returns `GraphQLSchema` instance as defined by `graphql` library.


## Required arguments

### `action`

```python
async def create_schema_hook(*types: BaseType) -> GraphQLSchema:
    ...
```

Next filter or built-in function used to create GraphQL schema.
