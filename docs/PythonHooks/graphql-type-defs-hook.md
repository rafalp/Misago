# `graphql_type_defs_hook`

`list` of `str` containing GraphQL type definitions in GraphQL Schema Definition Language that should be added to the GraphQL schema.


## Example

Add new type `Like` to GraphQL schema:

```python
from ariadne import gql
from misago.hooks import graphql_type_defs_hook


graphql_type_defs_hook.append(
    gql(
        """
            type Like {
                id: ID
                created_at: DateTime
                post: Post
            }

            extend type Post {
                likes: [Like]
            }
        """
    )
)
```