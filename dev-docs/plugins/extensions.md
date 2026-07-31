# Extensions

Consider the `ThreadDetailView` class that handles the thread page. It implements many different methods that depend on each other to display a thread page with posts, polls, quick reply form, and moderation actions.

It wouldn't make sense to implement a separate hook for each of those methods. This is where extensions step in. Extensions allow plugins to extend built-in Misago classes.


## Writing a custom extension

Let's implement a plugin that includes additional metadata in the thread page header: the number of users watching the thread.

The `ThreadDetailView` has a method named `get_header_meta` that it uses to retrieve a dict with metadata to display.

To extend this method, let's start with a basic extension in our plugin:

```python
# myplugin/extensions.py

from misago.metadata import TextMetadata
from misago.plugins import extends
from misago.threads.views import ThreadDetailView


@extends(ThreadDetailView)
class ThreadWatchersExtension:
    def get_header_meta(self, request, thread):
        data = super().get_header_meta(request, thread)
        data["items"].append(
            TextMetadata(
                id="watchers",
                text="21 watchers",
            )
        )

        return data
```

First, the plugin imports the necessary dependencies:

1. The `TextMetadata` data class that renders the string stored in its `text` attribute in metadata lists.
2. The `extends` decorator used to register extensions.
3. The `ThreadDetailView` built-in view to extend.

The plugin then registers the extension for the view:

```python
@extends(ThreadDetailView)
class ThreadWatchersExtension:
```

Finally, it overrides the view's `get_header_meta` method to include an item with the number of thread watchers:

```python
class ThreadWatchersExtension:
    def get_header_meta(self, request, thread):
        data = super().get_header_meta(request, thread)
        data["items"].append(
            TextMetadata(
                id="watchers",
                text="21 watchers",
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
    name = "thread_watchers"
    verbose_name = "Misago Thread Watchers Number Plugin"

    def ready(self):
        from . import extensions
```


### Displaying the real number of watchers

Currently, our extension includes static text in the thread metadata. To change this, we need to use the `WatchedThread` model from `misago.notifications.models` and count the number of objects related to the thread:

```python
# myplugin/extensions.py

from django.utils.translation import npgettext
from misago.metadata import TextMetadata
from misago.notifications.models import WatchedThread
from misago.plugins import extends
from misago.threads.views import ThreadDetailView


@extends(ThreadDetailView)
class ThreadWatchersExtension:
    def get_header_meta(self, request, thread):
        data = super().get_header_meta(request, thread)

        # Count the number of users who watch the thread
        watchers = WatchedThread.objects.filter(thread=thread).count()

        if not watchers:
            # Skip displaying watchers if none exist
            return data

        data["items"].append(
            TextMetadata(
                id="watchers",
                text=npgettext(
                    "thread meta bar watchers",
                    "%(number)s watcher",
                    "%(number)s watchers",
                    watchers,
                ) % {"number": watchers},
            )
        )

        return data
```

Now the plugin will display the number of users watching the thread on its page.
