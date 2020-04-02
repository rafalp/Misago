# `graphql_admin_type_defs_hook`

`list` of `str` containing GraphQL type definitions in GraphQL Schema Definition Language that should be added to the admin GraphQL schema.


## Example

Add new type `Like` to admin GraphQL schema:

```python
from ariadne import gql
from misago.hooks import graphql_admin_type_defs_hook


graphql_admin_type_defs_hook.append(
    gql(
        """
            type Like {
                id: ID
                created_at: DateTime
                post: Post
            }

            extend type Query {
                likes: [Like]
            }
        """
    )
)
```