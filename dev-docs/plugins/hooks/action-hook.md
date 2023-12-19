# Implementing an action hook

Action hooks gather multiple extra functions to call at a given point in Misago's logic. Depending on the individual hook, they may be used as event handlers, or they can return values of a predetermined type for later use.

This guide will show the entire process of adding an action hook to a pre-existing example function in Misago.


## The example function

Let's imagine a function that takes a `request` object and returns a `dict` with forum stats:

```python
from django.http import HttpRequest


def get_forum_stats(request: HttpRequest) -> dict[str, str]:
    return {}  # Function's body is not important to us in this example
```


## Creating `hooks` package

Hooks can be defined anywhere, but the convention used by Misago is to create a `hooks` package for every Django app that defines its own hooks.

Our example Django app looks like this:

```
stats_app/
    __init__.py
    stats.py
```

We will create a new Python package inside the `stats_app` and name it `hooks`:

```
stats_app/
    hooks/
        __init__.py
    __init__.py
    stats.py
```

Next, we will create an empty `get_stats.py` file in `hooks`:

```
stats_app/
    hooks/
        __init__.py
        get_stats.py
    __init__.py
    stats.py
```

Our hook's definition will be located in the `get_stats.py` file, but its instance will be re-exported from the `hooks/__init__.py` file.


## Minimal implementation

Misago's actions hooks are callable instances of classes extending the `ActionHook` type implemented by Misago and importable from `misago.plugins.hooks`:

```python
# get_stats.py
from misago.plugins.hooks import ActionHook


class GetStatsHook(ActionHook):
    __slots__ = ActionHook.__slots__  # important for memory usage!


get_stats_hook = GetStatsHook()
```

The above code is all that is needed to make our new hook work. If you are adding hooks to your plugin, this may be "good enough", but you should at least add annotations to the `GetStatsHook.__call__` method:

```python
# get_stats.py
from django.http import HttpRequest

from misago.plugins.hooks import ActionHook


class GetStatsHook(ActionHook):
    __slots__ = ActionHook.__slots__  # important for memory usage!

    def __call__(self, request: HttpRequest) -> list[dict[str, str]]:
        return super().__call__(request)


get_stats_hook = GetStatsHook()
```

We've added the `-> list[dict[str, str]]` annotation to the `__call__` method because the action hook gathers return values from called functions, and we want those to return a `dict[str, str]` with new stats to include in the `get_forum_stats` result.


## Adding type annotations

We will extend our hook to include type annotation for plugin functions it gathers ("actions"). This annotation will be a `Protocol`:

```python
# get_stats.py
from typing import Optional, Protocol

from django.http import HttpRequest

from misago.plugins.hooks import ActionHook


class GetStatsHookAction(Protocol):
    def __call__(self, request: HttpRequest) -> dict[str, str]:
        ...


class GetStatsHook(ActionHook[GetStatsHookAction]):
    __slots__ = ActionHook.__slots__  # important for memory usage!

    def __call__(self, request: HttpRequest) -> list[dict[str, str]]:
        return super().__call__(request)


get_stats_hook = GetStatsHook()
```

Those type annotations serve no function for the hook itself, but they are important for developers and tools. Developers now have an idea about how the hook, and the action functions that plugins can add to it look like.

Also, annotations enable type hints for this hook, which work with Python type checkers.

Finally, annotations enable documentation generation, which is a massive win for the maintainability of a project the size Misago is.


## Adding documentation

Misago's hooks documentation is generated from its code. Just the annotations that were added in the previous step will enable the generated document to show plugin developers how the hook and the function that they need to implement in their plugin look like.

Adding docstrings to those classes will result in the contents of those also being included in the generated document:

```python
# get_stats.py
from typing import Optional, Protocol

from django.http import HttpRequest

from misago.plugins.hooks import ActionHook


class GetStatsHookAction(Protocol):
    """
    This docstring will be placed under the `action`'s function signature 
    in the generated document.
    """

    def __call__(self, request: HttpRequest) -> dict[str, str]:
        ...


class GetStatsHook(ActionHook[GetStatsHookAction]):
    """
    This docstring will be placed at the start of the generated document.

    # Example

    Example sections will be extracted from this docstring 
    and placed at the end of the document.
    """

    __slots__ = ActionHook.__slots__  # important for memory usage!

    def __call__(self, request: HttpRequest) -> list[dict[str, str]]:
        return super().__call__(request)


get_stats_hook = GetStatsHook()
```

Docstrings can use Markdown formatting:

```python
class Example:
    """
    Lorem **ipsum** dolor
    sit amet elit.

    Another paragraph
    """
```

The above docstring will be converted by the documentation generator into:

> Lorem **ipsum** dolor sit amet elit.
> 
> Another paragraph


## Re-exporting hook from `hooks` package

Let's make our new hook directly importable from the `hooks` package we've created previously:

```python
# hooks/__init__.py
from .get_stats import get_stats_hook

__all__ = ["get_stats_hook"]
```

Now we will be able to import this hook with `from .hooks import get_stats_hook`.


## Updating core logic

With our hook completed, we can now update the original function to use it:

```python
from .hooks import get_stats_hook


def get_forum_stats(request: HttpRequest) -> dict[str, str]:
    forum_stats = {}  # Function's body is not important to us in this example

    # Add results from `get_stats_hook` to function's original result
    for result in get_stats_hook(request):
        forum_stats.update(result)

    return forum_stats
```

With this change the rest of the codebase that calls the `get_stats` function will now use its new version that includes plugins, without needing further changes.

If you don't like how `for result in get_stats_hook(request)` looks in new `get_forum_stats`, you can change hook's `__call__` to gather those stats into a single `dict`:

```python
# get_stats.py
from typing import Optional, Protocol

from django.http import HttpRequest

from misago.plugins.hooks import ActionHook


class GetStatsHookAction(Protocol):
    """
    This docstring will be placed under the `action`'s function signature 
    in the generated document.
    """

    def __call__(self, request: HttpRequest) -> dict[str, str]:
        ...


class GetStatsHook(ActionHook[GetStatsHookAction]):
    """
    This docstring will be placed at the start of the generated document.

    # Example

    Example sections will be extracted from this docstring 
    and placed at the end of the document.
    """

    __slots__ = ActionHook.__slots__  # important for memory usage!

    def __call__(self, request: HttpRequest) -> dict[str, str]:
        stats: dict[str, str] = {}
        for plugin_stats in super().__call__(request):
            stats.update(plugin_stats)
        return stats


get_stats_hook = GetStatsHook()
```

This allows us to limit the scale of changes to the `get_forum_stats` function:


```python
from .hooks import get_stats_hook


def get_forum_stats(request: HttpRequest) -> dict[str, str]:
    forum_stats = {}  # Function's body is not important to us in this example
    forum_stats.update(get_stats_hook(request))
    return forum_stats
```