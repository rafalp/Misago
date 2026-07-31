# Extensions

Consider the `ThreadDetailView` class that handles the thread page. It implements many different methods that depend on each other to display a thread page with posts, polls, quick reply form, and moderation actions.

It wouldn't make sense to implement a separate hook for each of those methods. This is where extensions step in. Extensions allow plugins to extend built-in Misago classes.


## Writing a custom extension

Let's implement a plugin that adds a link to the last post to the thread page header.

The `ThreadDetailView` has a method named `get_header_meta` that it uses to retrieve a dict with metadata to display.

To extend this method, let's start with a basic extension in our plugin:

```python
# myplugin/extensions.py

from misago.metadata import DatetimeMetadata
from misago.plugins import extends
from misago.threads.views import ThreadDetailView


@extends(ThreadDetailView)
class ThreadLastPostLinkExtension:
    def get_header_meta(self, request, thread):
        data = super().get_header_meta(request, thread)
        data["items"].append(
            DatetimeMetadata(
                id="last-post",
                text="Last post: %(datetime)s",
                datetime=thread.last_posted_at,
                url=self.get_post_last_url(thread),
            )
        )

        return data
```

First, the plugin imports the necessary dependencies:

1. The `DatetimeMetadata` data class that renders a date and time in metadata lists.
2. The `extends` decorator used to register extensions.
3. The `ThreadDetailView` built-in view to extend.

The plugin then registers the extension for the view:

```python
@extends(ThreadDetailView)
class ThreadLastPostLinkExtension:
```

Finally, it overrides the view's `get_header_meta` method to include the link to the last reply:

```python
class ThreadLastPostLinkExtension:
    def get_header_meta(self, request, thread):
        data = super().get_header_meta(request, thread)
        data["items"].append(
            DatetimeMetadata(
                id="last-post",
                text="Last post: %(datetime)s",
                datetime=thread.last_posted_at,
                url=self.get_post_last_url(thread),
            )
        )

        return data
```


### Loading extensions

Extensions are not loaded by default. You need to import them in your plugin app config's `ready` method:

```python
# myplugin/apps.py

from django.apps import AppConfig


class MyPluginConfig(AppConfig):
    name = "thread_last_post"
    verbose_name = "Misago Thread Last Post Link Plugin"

    def ready(self):
        from . import extensions
```


### `ExtensionRegistry`

Misago uses a single instance of `ExtensionRegistry` to store extensions and build extended types. This instance can be imported as `extensions` from the `misago.plugins` package:

```python
from misago.plugins import extensions
```


#### Methods

##### `ExtensionRegistry.register(base_type: type, extension_type: type, prepend: bool = False)`

Registers `extension_type` as an extension for `base_type`.

By default, new extensions are appended to the extension list. If `prepend=True`, the extension is inserted at the beginning of the list, making it the closest extension to the base class in the inheritance chain.

`extends` decorator is a small wrapper for this method and also supports the `prepend=True` option:

```python
@extends(ThreadDetailView, prepend=True)
class ThreadLastPostLinkExtension:
    ...
```


#### `ExtensionRegistry.get(base_type: type)`

Returns an extended type composed from `base_type` and its registered extensions. If no extensions are registered for `base_type`, returns `base_type` unchanged.

```python
ExtendedThreadListView = extensions.get(ThreadListView)
```

This method caches composed types. Registering a new extension invalidates the cached type for the affected base class.


### `extends()` decorator

The extends decorator is a small wrapper around the `ExtensionRegistry.register` method. It also supports the `prepend=True` option:

```python
@extends(ThreadDetailView, prepend=True)
class ThreadLastPostLinkExtension:
    ...
```

The decorator returns the decorated class unchanged, allowing the same extension to extend multiple classes:

```python
@extends(ThreadDetailView)
@extends(ThreadEditView)
@extends(ThreadPostEditView)
@extends(ThreadReplyView)
class GetThreadExtension:
    ...
```
