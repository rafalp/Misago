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


Moving forum configuration
--------------------------

To move configuration over to new forum, run ``python manage.py movesettings`` command.

.. note::
   Some settings have been moved from admin to configuration file, or removed. Those will not be migrated. Please consult :doc:`configuration reference </developers/settings>`.