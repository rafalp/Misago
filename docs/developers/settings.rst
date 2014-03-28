========
Settings
========


Accessing Settings
==================

Misago splits its settings into two groups:

* **Low level settings** - those settings must be available when Misago starts or control resources usage and shouldn't be changed frequently from admin control panel. Those settings live in ``settings.py``
* **High level settings** - those settings are stored in database and can be changed on runtime using interface provided by admin control panel.

Both types of settings can accessed as attributes of ``misago.conf.settings`` object and high level settings can be also accessed from your templates as attributes of ``misago_settings`` context value.

.. note::
   Not all high level settings values are available at all times. Some settings ("lazy settings"), are evaluated to ``True`` or ``None`` immediately upon load. This means while they can be checked to see if they have value or not, but require you to use special ``get_lazy_setting(setting)`` getter to actually obtain their real value.


Defining Custom DB Settings
===========================

.. note::
   Current Misago 0.6 migrations are south-based placeholders that will be replaced with new migrations introduced in Django 1.7 before release. For this reason this instruction focuses exclusively on usage of utility function provided by Misago.

In order to define or change high-level (stored in database) settings you have to add new rows to ``conf_settingsgroup`` and ``conf_settings`` database tables. This can be done by plenty of different ways, but preffered one is by creating new data migration and using functions from ``misago.conf.migrationutils`` module.


migrate_settings_group
----------------------

.. function:: migrate_settings_group(orm, group_fixture, old_group_key=None)

This function uses south supplied ORM instance to insert/update settings group in database according to provided dict contianing its name, description and contained settings. If new group should replace old one, you can provide its key in ``old_group_key`` argument.

The ``group_fixture`` dict should define following keys:

* **key** - string with settings group key.
* **name** - string with settings group name.
* **description** - optional string with short settings group description.
* **settings** - tuple containing dics describing settings belonging to this group.

Each dict in ``settings`` tuple should define following keys:

* **setting** - string with internal setting name.
* **name** - string with displayed setting name.
* **description** - optional string with small setting help message.
* **legend** - optional string indicating that before displaying this setting in form, new fieldset should be opened and this value should be used in its legend element.
* **python_type** - optional string defining type of setting's value. Can be either "string", "int", "bool" or "list". If omitted "string" is used by default.
* **value** - list, integer or string with default value for this setting.
* **form_field** - What form field should be used to change this setting. Can be either "text", "textarea", "select", "radio", "yesno" or "checkbox". If not defined, "text" is used. "checkbox" should be used exclusively for multiple choices list.
* **field_extra** - dict that defines extra attributes of form field. For "select", "radio" and "checkbox" fields this dict should contain "choices" key with tuple of tuples that will be used for choices in input. For "string" settings you can define "min_length" and "max_length" extra specifying minmal and maximal lenght of entered text. For integer settings you can specify minimal and maximal range in which value should fall by "min_value" and "max_value".


with_conf_models
----------------




Misago Settings Reference
=========================

By convention, low level settings are written in UPPER_CASE and high level ones are written in lower_case.


account_activation
------------------

Preffered way in which new user accounts are activated. Can be either of those:

* **none** - no activation required.
* **user** - new user has to click link in activation e-mail.
* **admin** - board administrator has to activate new accounts manually.
* **block** - turn new registrations off.


avatars_types
-------------

List of avatar sources available to users:

* **gravatar** -Gravatar.
* **upload** - avatar uploads.
* **gallery** - predefined gallery.


avatar_upload_limit
-------------------

Max allowed size of uploaded avatars in kilobytes.


default_avatar
--------------

Default avatar assigned to new accounts. Can be either ``gravatar`` or ``gallery`` which will make Misago pick random avatar from gallery instead.


default_timezone
----------------

Default timezone used by guests and newly registered users that haven't changed their timezone prefferences.


forum_name
----------

Forum name, displayed in default templates forum navbar and in titles of pages.


forum_index_meta_description
----------------------------

Forum index Meta Description used as value meta description attribute on forum index.


forum_index_title
-----------------

Forum index title. Can be empty string if not set, in which case ``forum_name`` should be used instead.


MISAGO_MAILER_BATCH_SIZE
------------------------

Default maximum size of single mails package that Misago will build before sending mails and creating next package.


password_complexity
-------------------

Complexity requirements for new user passwords. It's value is list of strings representing following requirements:

* **case** - mixed case.
* **alphanumerics** - both digits and letters.
* **special** - special characters.


password_length_min
-------------------

Minimal required length of new user passwords.


subscribe_reply
---------------

Default value for automaticall subscription to replied threads prefference for new user accounts. Its value represents one of those settings:

* **no** - don't watch.
* **watch** - put on watched threads list.
* **watch_email** - put on watched threads list and send e-mail when somebody replies.


subscribe_start
---------------

Default value for automaticall subscription to started threads prefference for new user accounts. Allows for same values as ``subscribe_reply``.


username_length_max
-------------------

Maximal allowed username length.


username_length_min
-------------------

Minimal allowed username length.
