# `thread_category_update_hook`

```python
from misago.graphql.public.mutations.hooks.threadcategoryupdate import thread_category_update_hook

thread_category_update_hook.call_action(
    action: ThreadCategoryUpdateAction,
    context: GraphQLContext,
    cleaned_data: ThreadCategoryUpdateInput,
)
```

A filter for the function used by `threadCategoryUpdate` GraphQL mutation to update the thread and its posts in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def thread_category_update(context: GraphQLContext, cleaned_data: ThreadCategoryUpdateInput) -> Thread:
    ...
```

Next filter or built-in function used to update the thread in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `thread` and `category` keys:

```python
class ThreadCategoryUpdateInput(TypedDict):
    thread: Thread
    category: Category
```