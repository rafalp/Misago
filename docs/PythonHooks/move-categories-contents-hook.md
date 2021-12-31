# `move_categories_contents_hook`

```python
from misago.categories.hooks import move_categories_contents_hook

move_categories_contents_hook.call_action(
    action: MoveCategoriesContentsAction,
    categories: Iterable[Category],
    new_category: Category,
)
```

A filter for the function used to move given categories contents to other category.

Returns `None`.


## Required arguments

### `action`

```python
async def move_categories_contents(
    categories: Iterable[Category], new_category: Category
):
    ...
```

Next filter or built-in function used to move given categories contents.


### `categories`

```python
Iterable[Category]
```

List of categories which content should be moved.


### `new_category`

```python
Category
```

Target category to which other categories contents should be moved to.
