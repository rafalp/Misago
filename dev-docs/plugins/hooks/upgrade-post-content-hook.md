# `upgrade_post_content_hook`

This hook wraps a standard Misago function used to upgrade post content after it has been posted.

The upgrade process runs in a Celery task scheduled after the post is created, allowing slow and costly operations, such as embedding previews of linked sites, to be performed without slowing down the posting process.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import upgrade_post_content_hook
```


## Filter

```python
def custom_upgrade_post_content_filter(action: UpgradePostContentHookAction, post: Post):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `post: Post`

The `Post` instance to update.


## Action

```python
def upgrade_post_content_action(post: Post):
    ...
```

Misago function used to upgrade post content or the next filter function from another plugin.


### Arguments

#### `post: Post`

The `Post` instance to update.


## Example

The code below implements a custom filter function that replaces custom plugin's HTML with new version:

```python
from misago.posting.hooks import upgrade_post_content_hook
from misago.threads.models import Post


@upgrade_post_content_hook.append_filter
def upgrade_post_plugin_html(action, post: Post):
    if "<plugin-html" in post.parsed:
        post.parsed = very_costful_html_change_operation(post.parsed)
        post.save(update_fields=["parsed"])

    action(post)
```