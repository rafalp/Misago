# `populate_post_feed_data_hook`

This hook wraps the standard function that Misago uses to populate post feed data using the `prefetched_data` dictionary.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import populate_post_feed_data_hook
```


## Filter

```python
def custom_populate_post_feed_data_filter(
    action: PopulatePostFeedDataHookAction,
    feed: list[dict],
    prefetched_data: dict,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: PopulatePostFeedDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `feed: list[dict]`

List of `dict`s representing post feed items.


#### `prefetched_data: dict`

`dict` containing data to populate the feed items with.


## Action

```python
def populate_post_feed_data_action(feed: list[dict], prefetched_data: dict):
    ...
```

Misago function used to populate post feed data using the `prefetched_data` dictionary.


### Arguments

#### `feed: list[dict]`

List of `dict`s representing post feed items.


#### `prefetched_data: dict`

`dict` containing data to populate the feed items with.


## Example

The code below implements a custom filter function that replaces post's displayed poster with a different one.

```python
from misago.threads.hooks import populate_post_feed_data_hook


@populate_post_feed_data_hook.append_filter
def replace_post_poster(
    action, feed: list[dict], prefetched_data: dict
):
    action(feed, prefetched_data)

    for item in feed:
        if (
            item["type"] == "post"
            and item["post"].plugin_data.get("override_poster")
        ):
            poster_id = item["post"].plugin_data.get("override_poster")
            item["poster"] = prefetched_data["users"].get(poster_id)
```