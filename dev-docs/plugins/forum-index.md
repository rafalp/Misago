Custom index pages
==================

Plugins can register custom views as new choices in the "index page" setting.


## Writing the view

Custom index view must accept the `is_index` keyword argument:

```python
# plugin/views.py
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def custom_view(
    request: HttpRequest, *args, is_index: bool | None = None, **kwargs
) -> HttpResponse:
    if not is_index and request.settings.index_view == "custom":
        # Redirect from view's standard url to index page if view is used by it
        return redirect(reverse("misago:index"))

    return HttpResponse("I am a custom view!")
```

This argument will be set to `True` when view is called for the index page.


## Adding the view to the choices

In the plugin's `AppConfig.ready` method, insert the code that will register its view as a new choice.

Available choices are stored on the `IndexViews` instance, which can be imported as `index_views` from the `misago.forumindex.views` module:

```python
# plugin/apps.py
from django.apps import AppConfig
from misago.forumindex.views import index_views

from .views import custom_view


class MisagoUsersOnlinePlugin(AppConfig):
    name = "misago_users_online_plugin"

    def ready(self):
        index_views.add_index_view("custom", custom_view)
```


## Adding fallback url when the view is not used as index

If the view should be available when its not selected as the forum index, create a custom `urls.py` file in your plugin with the `urlpattern` for it:

```
# plugin/urls.py

from django.urls import path

from .views import custom_view

urlpatterns = [
    path("custom-view/", custom_view, name="custom-view", kwargs={"is_index": False}),
]
```

You can skip this step otherwise.


## Adding the custom main menu item

The custom index page will also have to be added to the `main_menu` `Menu` instance that Misago uses to build the main menu:

```python
# plugin/apps.py
from django.apps import AppConfig
from django.utils.translation import pgettext_lazy
from misago.forumindex.menus import main_menu
from misago.forumindex.views import index_views

from .views import custom_view


class MisagoUsersOnlinePlugin(AppConfig):
    name = "misago_users_online_plugin"

    def ready(self):
        index_views.add_index_view("custom", custom_view)

        main_menu.add_item(
            key="custom",  # Same as index view `id_` arg 
            url_name="custom-view",  # Same as link name from prev step or `misago:index`
            label=pgettext_lazy("main menu item", "Custom"),
        )
```

When you do this, your new view will be available as `Custom` menu link, and Misago will make this link the first in the menu when it's selected as the index view.
