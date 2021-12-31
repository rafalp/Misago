# `graphql_types_hook`

A `list` of [Ariadne bindables](https://ariadnegraphql.org/docs/resolvers) that should be added to GraphQL API.


## Example

```python
from ariadne import TypeObject
from misago.graphql.hooks import graphql_types_hook
from misago.loaders import load_post


like_type = TypeObject("Like)


@like_type.field("post"):
async def resolve_like_post(obj, _):
    return await load_post(obj["post_id"])


graphql_types_hook.append(like_type)
```