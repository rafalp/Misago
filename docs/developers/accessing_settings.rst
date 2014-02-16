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
   Not all high level settings values are available at all times. Some settings, named lazy settings, can be checked to see if they have value defined, but require you to use special ``get_lazy_setting(setting)`` function to actually load it's value.


Misago Settings Reference
=========================

By convention, low level settings are written in UPPER_CASE and high level ones are written in lower_case.


forum_name
----------

Forum name.


forum_index_meta_description
-----------------

Forum index Meta Description used as value meta description attribute on forum index.


forum_index_title
-----------------

Forum index title. Can be empty string if not set, in which case ``forum_name`` should be used instead.


MISAGO_MAILER_BATCH_SIZE
------------------------

Default maximum size of single mails package that Misago will build before sending mails and creating next package.
