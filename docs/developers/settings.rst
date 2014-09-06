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
   Not all high level settings values are available at all times. Some settings ("lazy settings"), are evaluated to ``True`` or ``None`` immediately upon load. This means that they can be checked to see if they have value or not, but require you to use special ``get_lazy_setting(setting)`` getter to obtain their real value.


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
* **default_value** - if your setting should always have value, specify there fallabck value used if no user-defined value is available.
* **is_lazy** - if setting value may too large to be always loaded into memory, you may make setting lazily loaded by defining this key with ``True`` value assigned.
* **form_field** - What form field should be used to change this setting. Can be either "text", "textarea", "select", "radio", "yesno" or "checkbox". If not defined, "text" is used. "checkbox" should be used exclusively for multiple choices list.
* **field_extra** - dict that defines extra attributes of form field. For "select", "radio" and "checkbox" fields this dict should contain "choices" key with tuple of tuples that will be used for choices in input. For "string" settings you can define "min_length" and "max_length" extra specifying minmal and maximal lenght of entered text. For integer settings you can specify minimal and maximal range in which value should fall by "min_value" and "max_value". "textarea" field supports extra "rows" setting that controls generated textarea rows attribute. All text-based fields accept "required" setting. "checkbox" field supports "min" and "max" values that control minimum and maximum required choices.


.. note::
   If you wish to make your names and messages translateable, you should use ``ugettext_lazy`` function provided by Misago instead of Django one. This function is defined in ``misago.core.migrationutils`` module and differs from Django one by the fact that it preserves untranslated message on its ``message`` attribute.

   For your convience ``migrate_settings_group`` triess to switch translation messages with their "message" attribute when it writes to database and thus making their translation to new languages in future possible.


with_conf_models
----------------

.. function:: with_conf_models(migration, this_migration=None)

South migrations define special ``models`` attribute that holds dict representing structure of database at time of migration execution. This dict will by default contain only your apps models. To add settings models that ``migrate_settings_group`` requires to work, you have to use ``with_conf_models`` function. This function accepts two arguments:

* **migration** - name of migration in ``misago.conf`` app containing models definitions current for the time of your data migration.
* **this_migration** - dict with model definitions for this migration.

In addition to this, make sure that your migration ``depends_on`` attribute defines dependency on migration from ``misago.conf`` app::

    class Migration(DataMigration):

        # Migration code...

        models = with_conf_models('0001_initial', {
            # This migration models
        })

        depends_on = (
            ("conf", "0001_initial"),
        )


delete_settings_cache
---------------------

.. function:: delete_settings_cache()

If you have used ``migrate_settings_group`` function in your migration, make sure to call ``delete_settings_cache`` at its end to flush settings caches.


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


allow_custom_avatars
--------------------

Controls if users may set avatars from outside forums.


avatar_upload_limit
-------------------

Max allowed size of uploaded avatars in kilobytes.


default_avatar
--------------

Default avatar assigned to new accounts. Can be either ``initials`` for randomly generated pic with initials, ``gravatar`` or ``gallery`` which will make Misago pick random avatar from gallery instead.


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


MISAGO_ACL_EXTENSIONS
---------------------

List of Misago ACL framework extensions.


MISAGO_ADMIN_NAMESPACES
-----------------------

Link namespaces that are administrator-only areas that require additional security from Misago. Users will have to re-authenticate themselves to access those namespaces, even if they are already signed in your frontend. In addition they will be requested to reauthenticated if they were inactive in those namespaces for certain time.

Defautly ``misago:admin`` and ``admin`` namespaces are specified, putting both Misago and Django default admin interfaces under extended security mechanics.


MISAGO_ADMIN_PATH
-----------------

Path prefix for Misago administration backend. Defautly "admincp", but you may set it to empty string if you with to disable your forum administration backend.


MISAGO_ADMIN_SESSION_EXPIRATION
-------------------------------

Maximum allowed lenght of inactivity period between two requests to admin namespaces. If its exceeded, user will be asked to sign in again to admin backed before being allowed to continue activities.


MISAGO_ATTACHMENTS_ROOT
-----------------------

Path to directory that Misago should use to store post attachments. This directory shouldn't be accessible from outside world.


MISAGO_AVATAR_SERVER_PATH
-------------------------
Url path that that all avatar server urls starts with. If you are running Misago subdirectory, make sure to update it (i.e. valid path for  "http://somesite.com/forums/" is ``/forums/user-avatar``).


MISAGO_AVATAR_STORE
-------------------

Path to directory that Misago should use to store user avatars. This directory shouldn't be accessible from outside world.


MISAGO_AVATARS_SIZES
--------------------

Misago uses avatar cache that prescales avatars to requested sizes. Enter here sizes to which those should be optimized.


MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH
------------------------------------

Date format used by Misago ``compact_date`` filter for dates in this year.

Expects standard Django date format, documented `here <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date>`_


MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH_YEAR
-----------------------------------------

Date format used by Misago ``compact_date`` filter for dates in past years.

Expects standard Django date format, documented `here <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date>`_


MISAGO_DYNAMIC_AVATAR_DRAWER
----------------------------

Function used to create unique avatar for this user. Allows for customization of algorithm used to generate those.


MISAGO_MAILER_BATCH_SIZE
------------------------

Default maximum size of single mails package that Misago will build before sending mails and creating next package.


MISAGO_MARKUP_EXTENSIONS
------------------------

List of python modules extending Misago markup.


MISAGO_NOTIFICATIONS_MAX_AGE
----------------------------

Max age, in days, of notifications stored in database. Notifications older than this will be delted.


MISAGO_POSTING_MIDDLEWARES
--------------------------

List of middleware classes participating in posting process.


MISAGO_RANKING_LENGTH
---------------------

Some lists act as rankings, displaying users in order of certain scoring criteria, like number of posts or likes received.
This setting controls maximum age in days of items that should count to ranking.


MISAGO_SENDFILE_HEADER
----------------------

If your server provides proxy for serving files from application, like "X-Sendfile", set its header name in this setting.

Leave this setting empty to use Django fallback.


MISAGO_SENDFILE_LOCATIONS_PATH
------------------------------

Some Http servers (like Nginx) allow you to restrict X-Sendfile to certain locations.

Misago supports this feature with this setting, however with limitation to one "root" path. This setting is used for paths defined in ATTACHMENTS_ROOT and AVATAR_CACHE settings.

Rewrite algorithm used by Misago replaces path until last part with value of this setting.

For example, defining ``MISAGO_SENDFILE_LOCATIONS_PATH = 'misago_served_internals'`` will result in following rewrite:

``/home/mysite/www/attachments/13_05/142123.rar`` => ``/misago_served_internals/attachments/13_05/142123.rar``


password_complexity
-------------------

Complexity requirements for new user passwords. It's value is list of strings representing following requirements:

* **case** - mixed case.
* **alphanumerics** - both digits and letters.
* **special** - special characters.


password_length_min
-------------------

Minimal required length of new user passwords.


post_length_max
---------------

Maximal allowed post content length.


post_length_min
---------------

Minimal allowed post content length.


signature_length_max
--------------------

Maximal allowed length of users signatures.


subscribe_reply
---------------

Default value for automatic subscription to replied threads prefference for new user accounts. Its value represents one of those settings:

* **no** - don't watch.
* **watch** - put on watched threads list.
* **watch_email** - put on watched threads list and send e-mail when somebody replies.


subscribe_start
---------------

Default value for automatic subscription to started threads prefference for new user accounts. Allows for same values as ``subscribe_reply``.


thread_title_length_max
-----------------------

Maximal allowed thread title length.


thread_title_length_min
-----------------------

Minimal allowed thread title length.


username_length_max
-------------------

Maximal allowed username length.


username_length_min
-------------------

Minimal allowed username length.


Django Settings Reference
=========================

Django defines plenty of configuration options that control behaviour of different features that Misago relies on.

Those are documented and available in Django documentation: `Settings <https://docs.djangoproject.com/en/1.6/ref/settings/>`_
