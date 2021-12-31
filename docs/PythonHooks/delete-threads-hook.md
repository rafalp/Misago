# `delete_threads_hook`

```python
from misago.graphql.public.mutations.hooks.deletethreads import delete_threads_hook

delete_threads_hook.call_action(
    action: DeleteThreadsAction,
    context: GraphQLContext,
    cleaned_data: DeleteThreadsInput,
)
```

A filter for the function used by GraphQL mutation deleting threads to delete threads and their posts from the database.

Returns `None`.


## Required arguments

### `action`

```python
async def delete_threads(context: GraphQLContext, cleaned_data: DeleteThreadsInput):
    ...
```

Next filter or built-in function used to delete threads from the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `threads` key:

```python
class DeleteThreadsInput(TypedDict):
    threads: List[Thread]
```