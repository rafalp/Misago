# Implementing a filter hook

Filter hooks wrap the existing Misago functions. They can execute custom code before, after, or instead of the standard one.

This guide will show the entire process of adding a filter hook to a pre-existing example function in Misago.


## The example function

Let's imagine a function that parses a user-posted message into an HTML string:

```python
from django.http import HttpRequest


def parse_user_message(request: HttpRequest, message: str) -> str:
    return str(message)  # Function's body is not important to us in this example
```


## Creating `hooks` package

Hooks can be defined anywhere, but the convention used by Misago is to create a `hooks` package for every Django app that defines its own hooks.

Our example function lives in an example Django app, looking like this:

```
parser_app/
    __init__.py
    parser.py
```

We will create a new Python package inside the `parser_app` and name it `hooks`:

```
parser_app/
    hooks/
        __init__.py
    __init__.py
    parser.py
```

Next, we will create an empty `parse_user_message.py` file in `hooks`:

```
parser_app/
    hooks/
        __init__.py
        parse_user_message.py
    __init__.py
    parser.py
```

Our hook's definition will be located in the `parse_user_message.py` file, but its instance will be re-exported from the `hooks/__init__.py` file.


## Minimal implementation

Misago's filter hooks are callable instances of classes extending the `FilterHook` type implemented by Misago and importable from `misago.plugins.hooks`:

```python
# parse_user_message.py
from misago.plugins.hooks import FilterHook


class ParseUserMessageHook(FilterHook):
    __slots__ = FilterHook.__slots__  # important for memory usage!


parse_user_message_hook = ParseUserMessageHook()
```

The above code is all that is needed to make our new hook work. If you are adding hooks to your plugin, this may be "good enough", but you should at least add annotations to the `ParseUserMessageHook.__call__` method:

```python
# parse_user_message.py
from django.http import HttpRequest

from misago.plugins.hooks import FilterHook


class ParseUserMessageHook(FilterHook):
    __slots__ = FilterHook.__slots__  # important for memory usage!

    def __call__(
        self, action, request: HttpRequest, message: str
    ) -> str:
        return super().__call__(action, request, message)


parse_user_message_hook = ParseUserMessageHook()
```


## Adding type annotations

We will extend our hook to include type annotations for the original function this hook wraps (an "action") and for the filter functions it accepts from plugins ("filters"). Both of these annotations will be `Protocol`s:

```python
# parse_user_message.py
from typing import Optional, Protocol

from django.http import HttpRequest

from misago.plugins.hooks import FilterHook


class ParseUserMessageHookAction(Protocol):
    def __call__(self, request: HttpRequest, message: str) -> str:
        ...


class ParseUserMessageHookFilter(Protocol):
    def __call__(
        self, action: FilterUserDataHookAction, request: HttpRequest, message: str
    ) -> str:
        ...


class ParseUserMessageHook(
    FilterHook[ParseUserMessageHookAction, ParseUserMessageHookFilter]
):
    __slots__ = FilterHook.__slots__  # important for memory usage!

    def __call__(
        self, action: FilterUserDataHookAction, request: HttpRequest, message: str
    ) -> str:
        return super().__call__(action, request, message)


parse_user_message_hook = ParseUserMessageHook()
```

Those type annotations serve no function for the hook itself, but they are important for developers and tools. Developers now have an idea about how of the hook, the original function it wraps, and the filter functions that plugins can add to it look like.

Also, annotations enable type hints for this hook, which work with Python type checkers.

Finally, annotations enable documentation generation, which is a massive win for the maintainability of a project the size Misago is.


## Adding documentation

Misago's hooks documentation is generated from its code. Just the annotations that were added in the previous step will enable the generated document to show plugin developers how both the function wrapped by the hook and the function that they need to implement in their plugin look like.

Adding docstrings to those classes will result in the contents of those also being included in the generated document:

```python
# parse_user_message.py
from typing import Optional, Protocol

from django.http import HttpRequest

from misago.plugins.hooks import FilterHook


class ParseUserMessageHookAction(Protocol):
    """
    This docstring will be placed under the `action`'s function signature 
    in the generated document.
    """

    def __call__(self, request: HttpRequest, message: str) -> str:
        ...


class ParseUserMessageHookFilter(Protocol):
    """
    This docstring will be placed under the `filter`'s function signature 
    in the generated document.
    """

    def __call__(
        self, action: ParseUserMessageHookAction, request: HttpRequest, message: str
    ) -> str:
        ...


class ParseUserMessageHook(
    FilterHook[ParseUserMessageHookAction, ParseUserMessageHookFilter]
):
    """
    This docstring will be placed at the start of the generated document.

    # Example

    Example sections will be extracted from this docstring 
    and placed at the end of the document.
    """

    __slots__ = FilterHook.__slots__  # important for memory usage!

    def __call__(
        self, action: ParseUserMessageHookAction, request: HttpRequest, message: str
    ) -> str:
        return super().__call__(action, request, message)


parse_user_message_hook = ParseUserMessageHook()
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
from .parse_user_message import parse_user_message_hook

__all__ = ["parse_user_message"]
```

Now we will be able to import this hook with `from .hooks import parse_user_message_hook`.


## Updating core logic

With our hook completed, we can now update the code to use it. First, we will add the `_action` suffix to the original function's name:

```python
from django.http import HttpRequest


def parse_user_message_action(request: HttpRequest, message: str) -> str:
    return str(message)  # Function's body is not important to us in this example
```

Now we will create a shallow wrapper for this function, using its original name and signature:

```python
from django.http import HttpRequest


# Copied signature
def parse_user_message(request: HttpRequest, message: str) -> str:
    return parse_user_message_action(request, message)


# Original function
def parse_user_message_action(request: HttpRequest, message: str) -> str:
    return str(message)  # Function's body is not important to us in this example
```

Final step is updating our wrapper to use our new hook to call wrap all `parse_user_message_action` calls:

```python
from django.http import HttpRequest

from .hooks import parse_user_message_hook


# Copied signature
def parse_user_message(request: HttpRequest, message: str) -> str:
    return parse_user_message_hook(parse_user_message_action, request, message)


# Original function
def parse_user_message_action(request: HttpRequest, message: str) -> str:
    return str(message)  # Function's body is not important to us in this example
```

With this change the rest of the codebase that used the `parse_user_message` function will now call its new version that includes plugins, without needing further changes.

The original `parse_user_message_action` is still easily discernable, separate from the hook implementation.


## Disabling cache

`FilterHook` instances cache final reduced function on the first call. This works for regular functions and singleton methods, but will cause problems with filter hook's action is regular object's method as it will be cached and used in all future calls:

```python
class MyClass:
    def do_something(self):
        my_hook(self.do_something_action)

    def do_something_action(self):
        ...
```

For the above code, every future instance of the `MyClass` class will call the `do_something_action` method of the first `MyClass` instance to be created.

To avoid this issue, pass the `cache=False` option to your hook:

```python
parse_user_message_hook = ParseUserMessageHook(cache=False)
```
