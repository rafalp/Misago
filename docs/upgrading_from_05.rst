=========================
Upgrading from Misago 0.5
=========================

Misago 0.6 comes with special utility that allows those upgrading from Misago 0.5 to move their data to new site. This utility, named ``datamover``, provides set of management commands allowing you to move data over.


Preparing for move
==================

To move your data to new site, you'll need to first install Misago 0.6, and then tell mover how to access your old data.


Database
--------

In your site's ``settings.py`` find ``DATABASES`` setting, and add connection named ``misago05``::

    DATABASES = {
        'default': {
            # new database used by Misago
        },
        'misago05': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_misago_05_database_name',
            'USER': 'your_misago_05_database_user',
            'PASSWORD': 'your_misago_05_database_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }


User uploads
------------

You'll actually won't need all of your old forum's files for move, only attachments and media directories. To tell data mover where it can find those directories, add ``MISAGO_OLD_FORUM`` setting somewhere in your ``settings.py``, just like in example below::

    MISAGO_OLD_FORUM = {
        'ATTACHMENTS': '/home/somewhere/myoldmisago/attachments/',
        'MEDIA': '/home/somewhere/myoldmisago/media/',
    }


Creating superuser
------------------

Its good idea to create superuser accounts for all site administrators. Don't worry about their e-mails being same as ones on old forum. If this happens Misago will simply reuse those accounts, instead of creating new ones. 


Moving forum configuration
==========================

To move configuration over to new forum, run ``python manage.py movesettings`` command.

.. note::
   Some settings have been moved from admin to configuration file or removed. Those will not be migrated. Please consult :doc:`configuration reference </developers/settings>` for available settings that you will need to add yourself.


Moving users
============

To move users over to new forum, run ``python manage.py moveusers`` command.

Moved users will be assigned default rank and permissions as those aren't moved by the datamover. If user with such e-mail address already exists in database (because you've used this e-mail ealier to create superuser account), his or her permissions and rank will be left as they are in new database.

If user avatar could not be moved (for .eg because uploaded picture is smaller than allowed by ``MISAGO_AVATARS_SIZES``), default avatar will be set for this user.

In case of username collision, Misago will append digits to new user's username and print a warning in console to let you know about this.


Moving threads
==============

Todo


Wrapping up migration
=====================

Not everything is moved over. Thread labels will be turned into subcategories of their categories. With exception of pre-made superuser accounts, all users will be assigned to "Members" rank and will have only default roles of forum members. Likewise no permissions will be moved over to users, categories or ranks, and you will have to reset those manually. Reports and events will also be omitted by migration.


Recounting data
---------------

After moving users data over to new site, you'll need to rebuild their stats, trackers and bans. To do this use ``invalidatebans``, ``populateonlinetracker`` and ``synchronizeusers`` commands that you can run via ``manage.py``.

Likewise you'll need to rebuild threads and categories via ``synchronizethreads``, then ``synchronizecategories`` and ``rebuildpostssearch``.


Changed links
-------------

Todo