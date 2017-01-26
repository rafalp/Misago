Settings
========

Misago splits its settings into two groups:


## Core settings

Those settings must be available when Misago starts or control resources usage and shouldn't be changed frequently from admin control panel. Those settings live in settings.py

[Core settings reference](./Core.md)


## Database settings

Those settings are stored in database and can be changed on runtime using interface provided by admin control panel.

[Database settings reference](./Database.md)


## Accessing settings in template

Both types of settings can accessed as attributes of `misago.conf.settings` object and high level settings can be also accessed from your templates as attributes of `misago_settings` variable, like this:

```
<h1>{{ misago_settings.forum_name }}</h1> // will produce <h1>Misago Forums</h1>
```


##### Note

Not all high level settings values are available at all times. Some settings ("lazy settings"), are evaluated to True or None immediately upon load. This means that they can be checked to see if they have value or not, but require you to use special `settings.get_lazy_setting(setting)` getter to obtain their real value.


## Django Settings Reference

Django defines plenty of configuration options that control behaviour of different features that Misago relies on.

Those are documented and available in [Django documentation](https://docs.djangoproject.com/en/{{ book.django_version }}/ref/settings/).
