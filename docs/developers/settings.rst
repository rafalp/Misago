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
* **is_public** - public settings are included JSON that is passed to Ember.js application. Defaults to ``False``.
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


forum_branding_display
----------------------

Controls branding's visibility in forum navbar.


forum_branding_text
-------------------

Allows you to include text besides brand logo on your forum.


forum_name
----------

Forum name, displayed in titles of pages.


forum_index_meta_description
----------------------------

Forum index Meta Description used as value meta description attribute on forum index.


forum_index_title
-----------------

Forum index title. Can be empty string if not set, in which case ``forum_name`` should be used instead.


MISAGO_403_IMAGE
----------------

Url (relative to STATIC_URL) to file that should be served if user has no permission to see requested attachment.


MISAGO_404_IMAGE
----------------

Url (relative to STATIC_URL) to file that should be served if user has requested nonexistant attachment.


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


MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT
----------------------------------

Max dimensions (width and height) of user-uploaded images embedded in posts. If uploaded image is greater than dimensions specified in this settings, Misago will generate thumbnail for it.

.. note::
   Because user-uploaded GIF's may be smaller than dimensions specified, but still be considerably heavy due to animation, Misago always generates thumbnails for user-uploaded GIFS, stripping the animations from them.


MISAGO_ATTACHMENT_ORPHANED_EXPIRE
---------------------------------

How old (in minutes) should attachments unassociated with any be before they'll automatically deleted by ``clearattachments`` task.


MISAGO_ATTACHMENT_SECRET_LENGTH
-------------------------------

Length of attachment's secret (filenames and url token). The longer, the harder it is to bruteforce, but too long may conflict with your uploaded files storage limits (eg. filesystem path length limits).

.. warning::
   In order for Misago to support clustered deployments or CDN's (like Amazon's S3), its unable to validate user's permission to see the attachment at its source. Instead it has to rely on exessively long and hard to guess urls to attachments and assumption that your users will not "leak" source urls to attachments further.

   Generaly, neither you nor your users should use forums to exchange files containing valuable data, but if you do, you should make sure to secure it additionaly via other means like password-protected archives or file encryption solutions.


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


MISAGO_DIALY_POST_LIMIT
-----------------------

Dialy limit of posts that may be posted from single account. Fail-safe for situations when forum is flooded by spam bot. Change to 0 to lift this restriction.


MISAGO_DYNAMIC_AVATAR_DRAWER
----------------------------

Function used to create unique avatar for this user. Allows for customization of algorithm used to generate those.


MISAGO_HOURLY_POST_LIMIT
-----------------------

Hourly limit of posts that may be posted from single account. Fail-safe for situations when forum is flooded by spam bot. Change to 0 to lift this restriction.


MISAGO_LOGIN_API_URL
--------------------
URL to API endpoint used to authenticate sign-in credentials. Musn't contain api prefix or wrapping slashes. Defaults to 'auth/login'.


MISAGO_MAILER_BATCH_SIZE
------------------------

Default maximum size of single mails package that Misago will build before sending mails and creating next package.


MISAGO_MARKUP_EXTENSIONS
------------------------

List of python modules extending Misago markup.


MISAGO_NEW_REGISTRATIONS_VALIDATORS
-----------------------------------

List of functions to be called when somebody attempts to register on forums using registration form.


MISAGO_NOTIFICATIONS_MAX_AGE
----------------------------

Max age, in days, of notifications stored in database. Notifications older than this will be delted.


MISAGO_POST_ATTACHMENTS_LIMIT
-----------------------------

Limit of attachments that may be uploaded in single post. Lower limits may hamper image-heavy forums, but help keep memory usage by posting process. 


MISAGO_POSTING_MIDDLEWARES
--------------------------

List of middleware classes participating in posting process.


MISAGO_POSTS_PER_PAGE
---------------------

Controls number of posts displayed on thread page. Greater numbers can increase number of objects loaded into memory and thus depending on features enabled greatly increase memory usage.


MISAGO_POSTS_TAIL
-----------------

Defines minimal number of posts for thread's last page. If number of posts on last page is smaller or equal to one specified in this setting, last page will be appended to previous page instead.


MISAGO_RANKING_LENGTH
---------------------

Some lists act as rankings, displaying users in order of certain scoring criteria, like number of posts or likes received.
This setting controls maximum age in days of items that should count to ranking.


MISAGO_RANKING_SIZE
-------------------

Maximum number of items on ranking page.


MISAGO_READTRACKER_CUTOFF
-------------------------

Controls amount of data used by readtracking system. All content older than number of days specified in this setting is considered old and read, even if opposite is true. Active forums can try lowering this value while less active ones may wish to increase it instead.


MISAGO_SEARCH_CONFIG
--------------------

PostgreSQL text search configuration to use in searches. Defaults to "simple", for list of installed configurations run "\dF" in "psql".

Standard configs as of PostgreSQL 9.5 are: ``dutch``, ``english``, ``finnish``, ``french``, ``german``, ``hungarian``, ``italian``, ``norwegian``, ``portuguese``, ``romanian``, ``russian``, ``simple``, ``spanish``, ``swedish``, ``turkish``.

.. note::
   Example on adding custom language can be found `here <https://github.com/lemonskyjwt/plpstgrssearch>`_.

.. note::
   Items in Misago are usually indexed in search engine on save or update. If you change search configuration, you'll need to rebuild search for past posts to get reindexed using new configuration. Misago comes with ``rebuildpostssearch`` tool for this purpose.


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


MISAGO_STOP_FORUM_SPAM_USE
--------------------------

This settings allows you to decide wheter of not `Stop Forum Spam <http://www.stopforumspam.com/>`_ database should be used to validate IPs and emails during new users registrations.


MISAGO_STOP_FORUM_SPAM_MIN_CONFIDENCE
-------------------------------------

Minimum confidence returned by `Stop Forum Spam <http://www.stopforumspam.com/>`_ for Misago to reject new registration and block IP address for 1 day.


MISAGO_THREADS_ON_INDEX
--------------------------

Change this setting to ``False`` to display categories list instead of threads list on board index.


MISAGO_THREADS_PER_PAGE
---------------------

Controls number of threads displayed on page. Greater numbers can increase number of objects loaded into memory and thus depending on features enabled greatly increase memory usage.


MISAGO_THREADS_TAIL
------------------

Defines minimal number of threads for lists last page. If number of threads on last page is smaller or equal to one specified in this setting, last page will be appended to previous page instead.


MISAGO_THREAD_TYPES
-------------------

List of clasess defining thread types.


MISAGO_USERS_PER_PAGE
---------------------

Controls pagination of users lists.


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
