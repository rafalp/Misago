# `delete_thread_hook`

```python
from misago.graphql.public.mutations.hooks.deletethread import delete_thread_hook

delete_thread_hook.call_action(
    action: DeleteThreadAction,
    context: GraphQLContext,
    cleaned_data: DeleteThreadInput,
)
```

A filter for the function used by GraphQL mutation deleting thread to delete the thread and its posts from the database.

Returns `None`.


## Required arguments

### `action`

```python
async def delete_thread(context: GraphQLContext, cleaned_data: DeleteThreadInput):
    ...
```

Next filter or built-in function used to delete the thread from the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `thread` key:

```python
class DeleteThreadInput(TypedDict):
    thread: Thread
```