# `delete_categories_contents_hook`

```python
from misago.categories.hooks import delete_categories_contents_hook

delete_categories_contents_hook.call_action(
    action: DeleteCategoriesContentsAction,
    categories: Iterable[Category],
)
```

A filter for the function used to delete given categories contents from database.

Returns `None`.


## Required arguments

### `action`

```python
async def delete_categories_contents(categories: Iterable[Category]):
    ...
```

Next filter or built-in function used to delete given categories contents.


### `categories`

```python
Iterable[Category]
```

List of categories to remove contents of.
