# `get_posts_feed_item_user_ids_hook`

This hook enables plugins to include extra user IDs stored on posts in the query that Misago uses to retrieve `User`s to display on thread and private thread replies pages.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_posts_feed_item_user_ids_hook
```


## Action

```python
def custom_get_posts_feed_item_user_ids_filter(
    request: HttpRequest, item: dict, user_ids: set[int]
):
    ...
```

A function that finds user ids in the `item` and updates `user_ids` set with them.


### Arguments

#### `item: dict`

A `dict` with feed's item data.


#### `user_ids: set[int]`

A `set` of `int`s being user ids to retrieve from the database that action should mutate calling its `add` or `update` methods.


## Example

The code below implements a custom function that adds

```python
from misago.threads.hooks import get_posts_feed_item_user_ids_hook


@get_posts_feed_item_user_ids_hook.append_action
def include_plugin_users(
    item: dict,
    user_ids: set[int],
):
    if item["type"] != "post":
        return

    if linked_user_ids := item["plugin_data"].get("linked_posts_users"):
        user_ids.update(linked_user_ids)
```