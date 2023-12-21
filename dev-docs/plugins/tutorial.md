# Creating a custom plugin

Welcome to the plugin tutorial! In this tutorial, you will implement a "Users Online" plugin that will display a card containing a list of users currently online for site administrators on Misago's categories page. Additionally, this plugin will add a new page displaying all users currently online.

This exercise will cover all the basics of plugin development:

- Setting up a development environment for creating a new plugin.
- Getting a practical experience with Django templates, views, URLs, and the ORM.
- Using template outlets to include new HTML on existing pages.
- Adding a new page to the site.


## Django basics are required

Because Misago plugins are Django apps, knowledge of Django basics is necessary for plugin development.

If you don't know what Django apps are, how to use its ORM, create templates, views, or URLs, please see the ["First steps"](https://docs.djangoproject.com/en/5.0/#first-steps) section of the Django documentation. It provides a gentle and quick introduction to these concepts, which will be essential later.


## Misago development environment

To begin plugin development, clone the [Misago GitHub](https://github.com/rafalp/Misago) repository and run the `./dev init` command in your terminal. This will build the necessary Docker containers, install Python dependencies, and initialize the database. Once the command completes, you can start the development server using the `docker compose up` command.

Once the development server starts, visit http://127.0.0.1:8000/ in your browser to see your Misago site. You can sign in to the admin account using the `admin` and `password` credentials.

The `./dev` utility provides more commands than `init`. Run it without any arguments to get the list of all available commands.


## Initializing a minimal plugin

Look at the contents of the `plugins` directory. Misago's main repository comes with a few plugins already pre-installed. These plugins exist mainly to test the plugin system's features, but `minimal-plugin`, `full-manifest-plugin`, and the `misago-pypi-plugin` specified in the `pip-install.txt` file can be used as quick references for plugin developers.

Stop your development environment if it's running (`ctrl + c` or `cmd + c` in the terminal). Now, let's create a new directory for in `plugins` and name it `misago-users-online-plugin`. Inside of it, create another directory and name `misago_users_online_plugin`. Within this last directory, create two empty Python files: `__init__.py` and `misago_plugin.py`. Final directories structure should look like this:

```
misago-users-online-plugin/
    misago_users_online_plugin/
        __init__.py
        misago_plugin.py
```

This is the file structure of a minimal valid plugin that Misago will discover and load:

- `misago-users-online-plugin`: a directory containing all the plugin's files.
- `misago_users_online_plugin`: a Python package (and a Django application) that Misago will import.
- `__init__.py`: a file that makes the `misago_users_online_plugin` directory a Python package.
- `misago_plugin.py`: a file that makes the `misago_users_online_plugin` directory a Misago plugin.

It's important that the final plugin name and its Python package name are so close to each other. After the plugin is released to PyPI, Misago will build its imported Python package name from its PyPI name specified in the `pip-install.txt` file, using the `name.lower().replace("-", "_")` function. For example, the [Misago PyPI Plugin](https://pypi.org/project/misago-pypi-plugin/) is installable from PyPI as `misago-pypi-plugin`, but its Python package is named `misago_pypi_plugin` because that's the name Misago will try to include based on the `pip-install.txt` file contents.

The `misago-users-online-plugin` directory can contain additional files and directories. For example, it can include a `pyproject.toml` file with plugin's Python package data and dependencies. It can also include `requirements.txt` and `requirements-dev.txt` PIP requirements files. Requirements specified in those files will be installed during the Docker image build time. It is also possible (and recommended) to begin plugin development by creating a repository for it on GitHub or another code hosting platform and then cloning it to the `plugins` directory.


## Plugin list in admin control panel

Misago's admin control panel has a "Plugins" page that displays a list of all installed plugins on your Misago site. To access the admin control panel, start the development server with the `docker compose up` command and visit http://127.0.0.1:8000/admincp/ in your browser. You will see a login page for the Misago admin control panel. Log in using the `admin` username and `password` password.

After logging in, find the "Plugins" link in the menu on the left and click on it. The list of plugins should include our new plugin as "Misago-Users-Online-Plugin". If it's not there, make sure you've restarted the development server and that the plugin structure is correct.


## Plugin manifest

Misago will display a message next to our plugin that it's missing a manifest in its `misago_plugin.py` file. The plugin manifest is an instance of the `MisagoPlugin` data class populated with the plugin's data.

Let's update the `misago_plugin.py` file to include a basic manifest for our plugin:

```python
# misago_users_online_plugin/misago_plugin.py
from misago import MisagoPlugin


manifest = MisagoPlugin(
    name="Users Online",
    description="Displays users online list on the categories page.",
)
```

Save the updated file and refresh the admin's plugins page. Our plugin will now be displayed as "Users Online", along with a brief description of its functionality.

The `MisagoPlugin` class allows plugin authors to specify additional information about their plugins. Refer to the [plugin manifest reference](./plugin-manifest-reference.md) document for a comprehensive list of available fields.


## Application config

Because Misago's plugins are Django applications, we should add an [application config](https://docs.djangoproject.com/en/5.0/ref/applications/#for-application-authors) to our plugin. Application configs are especially useful for plugins using the hook system because of their [`ready`](https://docs.djangoproject.com/en/5.0/ref/applications/#django.apps.AppConfig.ready) callback method, which can be used to register new functions with hooks.

Create the `apps.py` file next to the `misago_plugin.py`, and define a config for our plugin:

```python
# misago_users_online_plugin/apps.py
from django.apps import AppConfig


class MisagoUsersOnlinePlugin(AppConfig):
    name = "misago_users_online_plugin"

    def ready(self):
        pass  # We will use the ready method soon!
```


## Displaying the "hello world" 

Let's add another file to our plugin that will hold the code adding our users online list to the categories page. We will name it `online_card.py`.

Inside this `online_card.py` file, we will include a function that returns a "Hello world!" string:

```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context


def users_online_card(request: HttpRequest, context: Context) -> str:
    return "Hello world!"
```

We need to add this function to a template outlet located under the categories list on the categories page. Referring to the [list of template outlets](./template-outlets-reference.md), we know that the outlet we need to use is named `CATEGORIES_LIST_END`. To achieve this, we'll utilize the [`append_outlet_action`](./template-outlets.md#append_outlet_action) from Misago to add our function to this outlet:


```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context
from misago.plugins.outlets import append_outlet_action


def users_online_card(request: HttpRequest, context: Context) -> str:
    return "Hello world!"


append_outlet_action("CATEGORIES_LIST_END", users_online_card)
```

We can also replace a hard-coded string with the outlet's name with the `PluginOutlet` enum value:

```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context
from misago.plugins.outlets import PluginOutlet, append_outlet_action


def users_online_card(request: HttpRequest, context: Context) -> str:
    return "Hello world!"


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

Lastly, we need to import `online_card.py` in the application config's `ready` method to actually run our code and register the function in an outlet:

```python
# misago_users_online_plugin/apps.py
from django.apps import AppConfig


class MisagoUsersOnlinePlugin(AppConfig):
    name = "misago_users_online_plugin"

    def ready(self):
        from . import online_card
```

Now, open http://127.0.0.1:8000/categories/ in your browser and scroll to the bottom of the page. You should see a "Hello world!" message being displayed right under the last category on the list.

If you can't see the message, double-check the `apps.py` and the `online_card.py` files. You may have to restart the developer server to ensure that those files are loaded.


## Returning an HTML from plugin function

Let's return to our `users_online_card` function. What will happen if we return an HTML string from it?

```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context
from misago.plugins.outlets import PluginOutlet, append_outlet_action


def users_online_card(request: HttpRequest, context: Context) -> str:
    return "<strong>Hello world!</strong>"


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

If we run the above code, we will see that the HTML was escaped:

```html
&lt;strong&gt;Hello world!&lt;/strong&gt;  
```

This is because our function returned a `str`, and those are, by default, escaped by Django's template engine. To disable this behavior, we need to mark this value as safe to display it without escaping. We can achieve this by using the `mark_safe` function from Django:

```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context
from django.utils.safestring import mark_safe
from misago.plugins.outlets import PluginOutlet, append_outlet_action


def users_online_card(request: HttpRequest, context: Context):
    return mark_safe("<strong>Hello world!</strong>")


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

Now our HTML is displayed correctly. But what if we want to mix HTML with unsafe values that need escaping? We could use the `escape` utility from Django's [`django.utils.html`](https://docs.djangoproject.com/en/5.0/ref/utils/#module-django.utils.html) module. However, a better option for this scenario is to use the [`format_html`](https://docs.djangoproject.com/en/5.0/ref/utils/#django.utils.html.format_html) utility:


```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context
from django.utils.html import format_html
from misago.plugins.outlets import PluginOutlet, append_outlet_action


def users_online_card(request: HttpRequest, context: Context):
    return format_html("<strong>{}</strong>", "Potentially insecure string")


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

Why not use a Django template? We could just `mark_safe` its markup because the unsafe values were already escaped for us by the Django template engine. In practice, parsing and rendering templates have a cost that can add up and cause a significant slow down when a plugin's outlet is used in multiple places (e.g., as part of a list item). In situations like that, it's useful for plugin developers to be aware of `format_html` as a faster alternative for rendering small bits of HTML.


## Rendering the online users card

Now that we know how to return HTML from our plugin function, let's actually implement a template because using `format_html` for displaying all our complex HTML is not really going to work.

We will create a `templates` directory in our plugin, and inside this directory we will create the `misago_users_online_plugin` directory with an `users_online_card.html` file:

```html
<!-- misago_users_online_plugin/templates/misago_users_online_plugin/users_online_card.html -->
<div class="panel panel-default panel-users-online">
    <div class="panel-heading">
        <h3 class="panel-title">Users online</h3>
    </div>
    <div class="panel-body">
        Hello world!
    </div>
</div>
```

Because our plugin is a Django application, Django will load templates from its `templates` directory without us having to do anything. However, if we place the `users_online_card.html` file directly in our plugin's templates, we risk a conflict with other plugins that also define such a file. This is why we created an additional `misago_users_online_plugin` directory in our plugin's `templates`. This extra directory will act as a namespace for our plugin's templates.

Now lets render this template in our plugin's function:

```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from misago.plugins.outlets import PluginOutlet, append_outlet_action


@mark_safe
def users_online_card(request: HttpRequest, context: Context):
    return render_to_string(
        "misago_users_online_plugin/users_online_card.html"
    )


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

When we refresh the categories page, we will see that our test message was replaced by our template's HTML. Now we need to implement logic to provide this template with a context. Let's start by displaying this card only to administrators:

```python
# misago_users_online_plugin/online_card.py
from django.http import HttpRequest
from django.template import Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from misago.plugins.outlets import PluginOutlet, append_outlet_action


@mark_safe
def users_online_card(request: HttpRequest, context: Context):
    if not request.user.is_staff:
        return ""

    return render_to_string(
        "misago_users_online_plugin/users_online_card.html"
    )


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

If we look at the page in anonymous browsing mode (or simply sign out), we will see that the card has disappeared. Note that we are returning an empty `str` instead of `None`. This is because the `mark_safe` decorator will cast the `None` value to a string saying `None`, which will then be displayed on the page. We don't want that!

Now, lets get the list of users who were online within last 15 minutes:

```python
# misago_users_online_plugin/online_card.py
from datetime import timedelta

from django.http import HttpRequest
from django.template import Context
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from misago.plugins.outlets import PluginOutlet, append_outlet_action
from misago.users.models import Online


@mark_safe
def users_online_card(request: HttpRequest, context: Context):
    if not request.user.is_staff:
        return ""

    users_online = Online.objects.filter(
        last_click__gte=timezone.now() - timedelta(minutes=15),
    ).select_related("user")

    return render_to_string(
        "misago_users_online_plugin/users_online_card.html",
        {"users_online": users_online},
    )


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

And lets update our template:

```html
<!-- misago_users_online_plugin/templates/misago_users_online_plugin/users_online_card.html -->
<div class="panel panel-default panel-users-online">
    <div class="panel-heading">
        <h3 class="panel-title">Users online</h3>
    </div>
    <div class="panel-body">
        {% for online in users_online %}
            <a href="{{ online.user.get_absolute_url }}" class="item-title">{{ online.user }}</a>{% if not forloop.last %}, {% endif %}
        {% endfor %}
    </div>
</div>
```

Now, you should see your own user appear on the online list. If you sign in to another user from another browser, they should appear too.

Currently, there are two issues with our plugin: it doesn't pass the global context from context processors to our template. If we try to access the `user`, it will always be `None`. We can solve this by passing the `request` as a third argument to `render_to_string`, but this will run all context processors again, which is expensive. Additionally, we can't pass the `Context` instance because `render_to_string` will raise an error if the context is not a `dict`. Worse, `render_to_string` parses the template to render on every call. If our plugin was called in a loop, the performance would take a serious hit.

Misago provides a special [`template_outlet_action`](./template-outlets.md#template_outlet_action-decorator) decorator, which deals with both of those issues. Let's update our plugin to use it:

```python
# misago_users_online_plugin/online_card.py
from datetime import timedelta

from django.http import HttpRequest
from django.template import Context
from django.utils import timezone
from misago.plugins.outlets import (
    PluginOutlet,
    append_outlet_action,
    template_outlet_action,
)
from misago.users.models import Online


@template_outlet_action
def users_online_card(request: HttpRequest, context: Context):
    if not request.user.is_staff:
        return None

    users_online = Online.objects.filter(
        last_click__gte=timezone.now() - timedelta(minutes=15),
    ).select_related("user")

    return (
        "misago_users_online_plugin/users_online_card.html",
        {"users_online": users_online},
    )


append_outlet_action(PluginOutlet.CATEGORIES_LIST_END, users_online_card)
```

The `template_outlet_action` decorator:

- Handles the returned `None` correctly, ensuring that nothing is rendered when the plugin's function returns it.
- Splits the tuple with a template name and context, merges this context with the global context, and then renders the template with it.
- Caches the parsed template on the `context` so it's not parsed multiple times.


## Adding localization

We should make our plugin use Django's localization features so that it supports multiple languages:

```html
<!-- misago_users_online_plugin/templates/misago_users_online_plugin/users_online_card.html -->
{% load i18n %}
<div class="panel panel-default panel-users-online">
    <div class="panel-heading">
        <h3 class="panel-title">{% trans "Users online" context "users online plugin" %}</h3>
    </div>
    <div class="panel-body">
        {% for online in users_online %}
            <a href="{{ online.user.get_absolute_url }}" class="item-title">{{ online.user }}</a>{% if not forloop.last %}, {% endif %}
        {% endfor %}
    </div>
</div>
```

Now, create an empty `locale` directory in the `misago_users_online_plugin`. This is the directory Django will load the plugin's translations from.

Finally, we will have to populate this directory with locale files. Run following command in your terminal:

```
./dev pluginmakemessages misago-users-online-plugin en
```

This will extract translation messages from your plugin's code and templates and will initialize an English locale for our plugin.

After translating the plugin, you will have to compile its messages:

```
./dev plugincompilemessages misago-users-online-plugin
```

Remember to repeat this process after all changes to translation messages in the plugin!


## Adding users online view

Let's learn how to use plugins to add new views to Misago. We will create a single view for our plugin: a list of users online, only accessible to the forum administrators.

First, we need to create a `views.py` file with a basic view that only displays a "Hello world!" message in a plain text:

```python
# misago_users_online_plugin/views.py
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello world!")
```

Now, let's create an `urls.py` file next to it with plugin's URLs:

```python
# misago_users_online_plugin/urls.py
from django.urls import path

from . import views

app_name = "users-online-plugin"
urlpatterns = [
    path("users-online/", views.index, name="index"),
]
```

Misago discovers and includes plugins' `urls.py` files automatically on server start. If you already have a running dev server, restart it.

After the development server has started, visit http://127.0.0.1:8000/users-online/ in your browser. You will see a "Hello world!" message from the plugin.

Now, let's update the `users_online_card.html` template to include a link to our new view:

```html
<!-- misago_users_online_plugin/templates/misago_users_online_plugin/users_online_card.html -->
{% load i18n %}
<div class="panel panel-default panel-users-online">
    <div class="panel-heading">
        <h3 class="panel-title">
            <a href="{% url 'users-online-plugin:index' %}">{% trans "Users online" context "users online plugin" %}</a>
        </h3>
    </div>
    <div class="panel-body">
        {% for online in users_online %}
            <a href="{{ online.user.get_absolute_url }}" class="item-title">{{ online.user }}</a>{% if not forloop.last %}, {% endif %}
        {% endfor %}
    </div>
</div>
```

The `app_name` in `urls.py` is used to define a namespace under which the URLs defined by the plugin will exist. Our plugin uses the `users-online-plugin` namespace and has a single URL named `index`. To reverse a URL to our view, we can use the `users-online-plugin:index` namespaced URL name.

Visit http://127.0.0.1:8000/categories/ in your browser and scroll down to the users online card. Its title will now be a link to our page.

Let's return to our view and update it to verify that the user visiting the page is an admin:

```python
# misago_users_online_plugin/views.py
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated or not request.user.is_staff:
        raise PermissionDenied(
            pgettext(
                "users online plugin",
                "You need to be an administrator to view this page.",
            )
        )

    return HttpResponse("Hello world!")
```

Let's walk through the new code line by line:

First, we check if the user is not authenticated or they are not an administrator (`is_staff` is Django's flag for administrator status).

Next, if the check passes (meaning the user can't view the page), we raise a `PermissionError` with a message about the missing administrator status.

[`pgettext`](https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#contextual-markers) is a translation message with a context specifying that it's a part of the `users online plugin`.

Visit http://127.0.0.1:8000/users-online/ without being signed in. Misago will display an error message informing us that the page we are trying to access is not available.

Let's change our model to actually fetch a list of users online in last 15 minutes and create a response from a template:

```python
# misago_users_online_plugin/views.py
from datetime import timedelta

from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import pgettext
from misago.users.models import Online


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated or not request.user.is_staff:
        raise PermissionDenied(
            pgettext(
                "users online plugin",
                "You need to be an administrator to view this page.",
            )
        )

    users_online = Online.objects.filter(
        last_click__gte=timezone.now() - timedelta(minutes=15),
    ).select_related("user")

    return render(
        request,
        "misago_users_online_plugin/index.html",
        {"users_online": users_online},
    )
```

Finally, create a `misago_users_online_plugin/index.html` template file with those contents:

```html
{% extends "misago/base.html" %}
{% load i18n misago_batch %}


{% block title %}
  {% trans "Users online" context "users online plugin" %} | {{ block.super }}
{% endblock title %}


{% block content %}
<div class="page page-users-online">
  <div class="container page-header-container">
    <div class="page-header page-header-users-online">
      <div class="page-header-bg-image">
        <div class="page-header-bg-overlay">
          <div class="page-header-image"></div>
          <div class="page-header-banner page-header-banner-users-online">
            <div class="page-header-banner-bg-image">
              <div class="page-header-banner-bg-overlay">
                <h1>{% trans "Users online" context "users online plugin" %}</h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="container page-container">
    {% for row in users_online|batch:4 %}
      <div class="row">
        {% for user_online in row %}
          <div class="col-xs-12 col-md-3">
            <a href="{{ user_online.user.get_absolute_url }}" class="item-title">{{ user_online.user }}</a>
            <br />
            <span misago-timestamp="{{ user_online.last_click.isoformat }}">
              {{ user_online.last_click|date:"DATETIME_FORMAT" }}
            </span>
          </div>
        {% endfor %}
      </div>
    {% endfor %}
  </div>
</div>
{% endblock content %}
```

Refresh the users online page. It will now contain a simple list of user names, together with the timestamp of their last click.

Here are some parts of the template explained:

`{% block title %}` defaults to `{{ settings.forum_name }}` as a default page title. We are using Django's template inheritance to prepend the "Users online" text before it.

`|batch:4` is a custom filter loaded from `misago_batch`. This filter splits an iterable into an iterable of iterables, which is very helpful when a grid system is used. Misago uses a Bootstrap version that requires for every row of the grid to be wrapped in a `<div class="row"></div>` HTML, and displays no more than 4 users per row.

`misago-timestamp="{{ user_online.last_click.isoformat }}"` is a custom HTML attribute specific to Misago's JavaScript. The presence of this attribute tells the UI that this element displays a timestamp that should be updated every minute with a relative timestamp from the `user_online.last_click.isoformat` value. `{{ user_online.last_click|date:"DATETIME_FORMAT" }}` is a default displayed timestamp as full date time, shown to the clients without JavaScript.


## Note about tutorial plugin's utility

The plugin we've created over the course of this tutorial can be used in production, but it has performance issues that limit its utility only to small forums. Without an index on the `last_click` column, which would make filtering faster when the online table contains entries for thousands of users, finding only users who were active within the last 15 minutes will be very slow on medium to large forums.

Other developers are welcome to use this plugin as a base for implementing a "proper" plugin with an online users list that will be safe to use in production on all forums.


## Completed plugin code

A repository with completed plugin's code is available on [GitHub](https://github.com/rafalp/misago-users-online-plugin).