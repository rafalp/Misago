# Extending Misago

Misago defines a multiple extension points that plugin developers can use to add new features to Misago and extend or customize existing ones.


## Plugins are Django applications

Misago plugins are [Django applications](https://docs.djangoproject.com/en/5.0/ref/applications/) with some additional functionality.

All standard Django extension points work out of the box in Misago plugins:

- App config in the `apps.py` file.
- Models defined in the `models.py` file.
- Database migrations in the `migrations` directory.
- Translations in the `locale` directory.
- Templates in the `templates` directory.
- Template tags in the `templatetags` directory.
- Static files in the `static` directory.


## App configs

Plugin should define an [application config](https://docs.djangoproject.com/en/5.0/ref/applications/#for-application-authors). The [`ready`](https://docs.djangoproject.com/en/5.0/ref/applications/#django.apps.AppConfig.ready) method should be used to register extensions in Misago:

```python
# my_plugin/apps.py
from django.apps import AppConfig
from misago.oauth2.hooks import validate_user_data_hook

from .validators import validate_user_forum_permissions


class MyPluginConfig(AppConfig):
    name = "my_plugin"
    verbose_name = "My Plugin"

    def ready(self):
        # Register functions in hooks directly in `ready()`
        validate_user_data_hook.append_filter(validate_user_forum_permissions)

        # Or import a Python module to execute its logic
        from . import validators as _
```


## Hooks

Hooks are predefined locations in Misago's code where plugins can inject custom Python functions to execute as part of Misago's standard logic.

- [Hooks guide](./hooks/index.md)
- [Built-in hook reference](./hooks/reference.md)


## Template outlets

Template outlets are special hooks located in Misago's templates where plugins can include extra HTML.

- [Template outlets guide](./template-outlets.md)
- [Built-in template outlets reference](./template-outlets-reference.md)


## Templates

Plugins can define custom templates in their `templates` directory. Those templates should be namespaced by keeping them in an extra directory within `templates`, e.g.:

```
# Good:
my_plugin/
  templates/
    my_plugin/
      template.html

# Bad:
my_plugin/
  templates/
    template.html
```


### Overriding default templates

If a plugin defines a template with the same path and file as a template that already exists in Misago, the plugin's template will be loaded instead of Misago's.

For example, a plugin that replaces Misago's navbar with a custom one should have a `navbar.html` template in its `templates/misago` directory:

```
my_plugin/
  templates/
    misago/
      navbar.html
```

Note that site owners can still override Misago and plugin templates through the `theme/templates` directory, which is part of the `misago-docker` setup.


## Plugin data

Some of Misago models have a special `plugin_data` JSON field that defaults to an empty JSON object (`{}`). This field can be used as a convenient storage space for plugins to store their data on Misago objects. Additionally, a GIN index is created on this field, allowing it to be [used in queries](https://docs.djangoproject.com/en/5.0/topics/db/queries/#querying-jsonfield).

The following models currently define this field:

- `misago.categories.models.Category`
- `misago.threads.models.Attachment`
- `misago.threads.models.AttachmentType`
- `misago.threads.models.Poll`
- `misago.threads.models.Post`
- `misago.threads.models.Thread`
- `misago.users.models.Group`
- `misago.users.models.User`

`plugin_data` is not a replacement for models. Use it for [denormalization](https://en.wikipedia.org/wiki/Denormalization), storing small bits of data that are frequently accessed or used in queries. 


## URLs

Plugin [`urls`](https://docs.djangoproject.com/en/5.0/topics/http/urls/#example) modules are automatically [included](https://docs.djangoproject.com/en/5.0/topics/http/urls/#including-other-urlconfs) in the site's `urlconf` before `misago.urls`.

If both Misago and a plugin define a URL with the same path, the plugin's URL takes precedence over Misago's. This enables plugins to replace Misago's URLs and views.

By default, included plugin URLs are not namespaced. If you want your plugin's URLs to be namespaced, you need to [define the namespace](https://docs.djangoproject.com/en/5.0/topics/http/urls/#url-namespaces-and-included-urlconfs) in your plugin's URLs module.


## Notifications

The Notifications document provides a guide for adding custom notifications to Misago:

[Adding custom notifications](../notifications.md#adding-custom-notification)
