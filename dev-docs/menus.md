Menus
=====

`Menu` based menus
------------------

Some menus in Misago are using the `Menu` class importable from `misago.menus.menu` module. Those menus are:

- Account settings menu
- Profile sections menu
- Users lists menu


### Creating custom menu with `Menu`

To create custom menu with `Menu`, instantiate it somewhere in your package:

```python
# my_plugin/menu.py
from django.utils.translation import pgettext_lazy
from misago.menus.menu import Menu

plugin_menu = Menu()
```

Next, add new menu items to it:

```python
# my_plugin/menu.py
from misago.menus.menu import Menu

plugin_menu = Menu()

plugin_menu.add_item(
    key="scores",
    url_name="my-plugin:scores",
    label=pgettext_lazy("my plugin menu", "Scores"),
)
plugin_menu.add_item(
    key="totals",
    url_name="my-plugin:totals",
    label=pgettext_lazy("my plugin menu", "Totals"),
)
```

To get list of menu items to display in template, call `get_items` method with Django's `HttpRequest` instance:

```python
# my_plugin.views.py
from django.shortcuts import render

from .menu import plugin_menu

def my_view(request):
    render(request, "my_plugin/template.html", {
        "menu": plugin_menu.get_items(request)
    })
```


### `Menu.add_item` method

`Menu.add_item` method adds new item to the menu. It requires following named arguments:

- `key`: a `str` identifying this menu item. Must be unique in whole menu.
- `url_name`: a `str` with URL name to `reverse` into final URL.
- `label`: a `str` or lazy string object with menu item's label.

`add_item` method also accepts following optional named arguments:

- `icon`: a `str` with icon to use for this menu item.
- `visible`: a `callable` accepting single argument (Django's `HttpRequest` instance) that should return `True` if this item should be displayed.

By default, menu items are added at the end of menu. To insert item before or after the other one, pass it's key to the `after` and `before` optional named argument:

```python
plugin_menu.add_item(
    key="scores",
    url_name="my-plugin:scores",
    label=pgettext_lazy("my plugin menu", "Scores"),
)

# Totals will be inserted before Scores
plugin_menu.add_item(
    key="totals",
    url_name="my-plugin:totals",
    label=pgettext_lazy("my plugin menu", "Totals"),
    before="scores",
)
```


### `Menu.get_items` method

`Menu.get_items` requires single argument, an instance of Django's `HttpRequest` and returns a Python `list`` of all visible menu items with their URL names reversed to URLs and `label`s casted to `str`. Each list item is an instance of frozen dataclass with following attributes:

- `active`: a `bool` specifying if this item is currently active.
- `key`: a `str` with item's key.
- `url`: a `str` with reversed URL.
- `label`: a `str` with item's label.
- `icon`: a `str` with item's icon or `None`.