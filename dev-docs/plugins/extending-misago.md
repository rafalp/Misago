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
- Static files in the `static` directory.


## Hooks

Hooks are predefined locations in Misago's code where plugins can inject custom Python functions to execute as part of Misago's standard logic.

- [Hooks guide](./hooks/index.md)
- [Built-in hook reference](./hooks/reference.md)


## Plugin data

Some of Misago models have a special `plugin_data` JSON field that defaults to an empty JSON object (`{}`). This field can be used as a convenient storage space for plugins to store their data on Misago objects. Additionally, a GIN index is created on this field, allowing it to be [used in queries](https://docs.djangoproject.com/en/5.0/topics/db/queries/#querying-jsonfield).

The following models currently define this field:

- `misago.categories.models.Category`
- `misago.threads.models.Attachment`
- `misago.threads.models.AttachmentType`
- `misago.threads.models.Poll`
- `misago.threads.models.Post`
- `misago.threads.models.Thread`
- `misago.users.models.User`

`plugin_data` is not a replacement for models. Use it for [denormalization](https://en.wikipedia.org/wiki/Denormalization), storing small bits of data that are frequently accessed or used in queries. 


## Urls

Plugin [`urls`](https://docs.djangoproject.com/en/5.0/topics/http/urls/#example) modules are automatically [included](https://docs.djangoproject.com/en/5.0/topics/http/urls/#including-other-urlconfs) in the site's `urlconf` before `misago.urls`.

If both Misago and a plugin define a URL with the same path, the plugin's URL takes precedence over Misago's. This enables plugins to replace Misago's URLs and views.

By default, included plugin URLs are not namespaced. If you want your plugin's URLs to be namespaced, you need to [define the namespace](https://docs.djangoproject.com/en/5.0/topics/http/urls/#url-namespaces-and-included-urlconfs) in your plugin's URLs module.


## Notifications

The Notifications document provides a guide for adding custom notifications to Misago:

[Adding custom notifications](../notifications.md#adding-custom-notification)

