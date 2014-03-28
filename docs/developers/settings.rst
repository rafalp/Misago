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


Defining Custom Settings
========================


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
