# Template outlets

Template outlets are special hooks located in Misago's templates where plugins can include extra HTML.


## Template outlet function

Functions registered in template outlets are called with two arguments: the `request` object and a `django.template.Context` instance, and return either `str`, `SafeText` or `None`:

```python
from django.http import HttpRequest
from django.template import Context
from django.utils.html import format_html
from django.utils.safestring import SafeText

from misago.threads.models import Post, Thread
from misago.users.models import User


def display_forum_stats(request: HttpRequest, context: Context) -> SafeText:
    return format_html(
        (
            "<ul class=\"forum-stats\">"
            "<li>Threads: <strong>{}</strong></li>"
            "<li>Posts: <strong>{}</strong></li>"
            "<li>Users: <strong>{}</strong></li>"
            "</ul>"
        ),
        Thread.objects.count(),
        Post.objects.count(),
        User.objects.count(),
    )
```


### Conditional rendering

A function can return `None` to don't render anything in a template outlet:

```python
from django.http import HttpRequest
from django.template import Context
from django.utils.html import format_html
from django.utils.safestring import SafeText

from misago.threads.models import Post, Thread
from misago.users.models import User


def display_forum_stats(request: HttpRequest, context: Context) -> SafeText | None:
    # Hide forum stats from unregistered users
    if context["user"].is_anonymous:
        return None

    return format_html(
        (
            "<ul class=\"forum-stats\">"
            "<li>Threads: <strong>{}</strong></li>"
            "<li>Posts: <strong>{}</strong></li>"
            "<li>Users: <strong>{}</strong></li>"
            "</ul>"
        ),
        Thread.objects.count(),
        Post.objects.count(),
        User.objects.count(),
    )
```


### Automatic escaping

If the function returns a `str`, it will be automatically escaped before its insertion in a template:

```python
def display_hello_message(request: HttpRequest, context: Context) -> str:
    return (
        f"<div class=\"alert alert-info\">Welcome, {context['user'].username}!</div>"
    )
```

Produces escaped HTML:

```html
&lt;div class=&quot;alert alert-info&quot;&gt;Welcome, John!&lt;/div&gt;
```

To prevent this escaping, use the [`format_html`](https://docs.djangoproject.com/en/5.0/ref/utils/#django.utils.html.format_html) and [`mark_safe`](https://docs.djangoproject.com/en/5.0/ref/utils/#django.utils.safestring.mark_safe) utilities from Django.

Especially, `mark_safe` is useful if your function renders a template as its output:

```python
from django.http import HttpRequest
from django.template import Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from misago.threads.models import Post, Thread
from misago.users.models import User


@mark_safe
def display_forum_stats(request: HttpRequest, context: Context) -> str:
    forum_stats = {
        "threads": Thread.objects.count(),
        "posts": Post.objects.count(),
        "users": User.objects.count(),
    }

    return render_to_string("my_plugin/forum_stats.html", forum_stats)
```

Note that when a function decorated with `mark_safe` returns `None`, it will be cast to a `str` and displayed in a template. Instead, return an empty string when using the `mark_safe` decorator.


## `template_outlet_action` decorator

The `display_forum_stats` function from the previous section can be simplified with the `template_outlet_action` decorator:

```python
from typing import Tuple

from django.http import HttpRequest
from django.template import Context

from misago.plugins.outlets import template_outlet_action
from misago.threads.models import Attachment, Post, Thread
from misago.users.models import User


@template_outlet_action
def display_forum_stats(request: HttpRequest, context: Context) -> Tuple[str, dict]:
    return (
        "my_plugin/forum_stats.html",
        {
            "threads": Thread.objects.count(),
            "posts": Post.objects.count(),
            "users": User.objects.count(),
        }
    )
```

`template_outlet_action` behaves differently based on the return value of the decorated function:

If a function returns a `str`, this string is used as the template name, which is then rendered with the unchanged context.

If a tuple of `str` and `dict` is returned, the string is used as a template name, and the dictionary is used to update the context before rendering the template.

If `None` is returned, nothing is rendered.

This enables advanced use cases:

```python
from typing import Tuple

from django.http import HttpRequest
from django.template import Context

import misago
from misago.plugins.outlets import template_outlet_action
from misago.threads.models import Post, Thread
from misago.users.models import User


@template_outlet_action
def display_forum_stats(request: HttpRequest, context: Context) -> Tuple[str, dict] | None:
    # Hide forum stats from unregistered users
    if request.user.is_anonymous:
        return None

    forum_stats = {
        "threads": Thread.objects.count(),
        "posts": Post.objects.count(),
        "users": User.objects.count(),
    }

    # Display full forum stats for admins
    if request.user.is_staff:
        forum_stats.update({
            "attachments": Attachment.objects.count(),
            "misago": misago.__version__,
        })
        return ("my_plugin/forum_stats_admins.html", forum_stats)

    return ("my_plugin/forum_stats.html", forum_stats)
```


## Registering a function in an outlet

To register a function in a template outlet, use the `append_outlet_action` or `prepend_outlet_action` functions from the `misago.plugins.outlets` module:

```python
from misago.plugins.outlets import append_outlet_action


def display_forum_stats(request: HttpRequest, context: Context):
    ...


append_outlet_action("OUTLET_NAME", display_forum_stats)
```


### `append_outlet_action`

```python
def append_outlet_action(
    outlet_name: str | PluginOutlet,
    function: Callable[[Context], str | SafeText],
):
    ...
```

This function registers a `function` at the end of the functions list for the `outlet_name` outlet.


### `prepend_outlet_action`

```python
def prepend_outlet_action(
    outlet_name: str | PluginOutlet,
    function: Callable[[Context], str | SafeText],
):
    ...
```

This function registers a `function` at the start of the functions list for the `outlet_name` outlet.


## Built-in template outlets

A list of all built-in template outlets generated from the Misago source code is available in a separate document:

[Built-in template outlets reference](./template-outlets-reference.md)


## Template tags

Template outlets in templates are realized with two template tags, loadable from `misago_plugins`.


### `pluginoutlet`

The `{% pluginoutlet OUTLET %}` template tag calls functions registered with the `OUTLET` template outlet and inserts the `str` and `SafeText` returned from them in the rendered template:

```html
{% load misago_plugins %}

{% pluginoutlet OUTLET %}
```


### `hasplugins`

The `{% hasplugins OUTLET %}` template tag works like Django's standard `{% if CONDITION %}` tag but only renders content if the specified template outlet has any functions registered with it.

Sample usage:

```html
{% load misago_plugins %}

{% hasplugins OUTLET %}
    <div class="plugin-menu">{% pluginoutlet OUTLET %}</div>
{% endhasplugins %}
```

The `{% else %}` clause is also supported for displaying alternative content if no functions are registered with the outlet:

```html
{% load misago_plugins %}

{% hasplugins OUTLET %}
    <div class="plugin-menu">{% pluginoutlet OUTLET %}</div>
{% else %}
    <div class="plugin-menu-disabled">This menu is not available</div>
{% endhasplugins %}
```


## Adding new template outlets

To create a new template outlet, use the `create_new_outlet` function from the `misago.plugins.outlets` module:

```python
from misago.plugins.outlets import create_new_outlet

create_new_outlet("MY_OUTLET")
```

Next, insert a `{% pluginoutlet MY_OUTLET %}` tag in a template:

```html
{% load misago_plugins %}
<!-- Some template content -->
{% pluginoutlet MY_OUTLET %}
<!-- Other template content -->
```

If you are contributing a new outlet in a pull request to Misago, instead of using `create_new_outlet`, update the `PluginOutlet` enumerable defined in `misago.plugins.enums`:

```python
class PluginOutlet(Enum):
    # ...

    NEW_OUTLET = "Short note describing new outlet's location."
```

Misago's default template outlets are automatically created from this enumerable.
