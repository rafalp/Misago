======
Misago
======

.. image:: https://travis-ci.org/rafalp/Misago.svg?branch=master
   :target: https://travis-ci.org/rafalp/Misago
   :alt: Tests Result

.. image:: https://coveralls.io/repos/github/rafalp/Misago/badge.svg?branch=master
   :target: https://coveralls.io/github/rafalp/Misago?branch=master
   :alt: Test Coverage

.. image:: https://badges.gitter.im/Misago/Misago.svg
   :target: https://gitter.im/Misago/Misago?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
   :alt: Development Chat

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
   :target: https://travis-ci.org/rafalp/Misago
   :alt: Works on Python 2.7, 3.5, 3,6


**Development Status: `Banans <https://en.wikipedia.org/wiki/Perpetual_beta>`_**

Misago aims to be complete, featured and modern forum solution that has no fear to say 'NO' to common and outdated opinions about how forum software should be made and what it should do.

* **Homepage:** http://misago-project.org/
* **Documentation:** https://rafalp.gitbooks.io/misago/
* **Code & BugTracker:** https://github.com/rafalp/Misago/


Screenshots
===========

.. image:: https://misago-project.org/media/mporg-home-small.png
   :target: https://misago-project.org
   :alt: Forum index

.. image:: https://misago-project.org/media/mporg-thread-small.png
   :target: https://misago-project.org
   :alt: Thread view


Production use
==============

As of now Misago implements all features considered "must have" on live internet forum:

* Your users may register accounts, set avatars, change options and edit their profiles. They have option to reset forgotten password.
* Site admins may require users to confirm validity of their e-mail addresses via e-mail sent activation link, or limit user account activation to administrator action. They can use custom Q&A challenge, ReCAPTCHA, Stop Forum Spam or IP's blacklist to combat spam registrations. Pletora of settings are available to control user account behaviour, like username lengths or avatar restrictions.
* Create categories together with unlimited number and depth of subcategories.
* Write messages using either GitHub flavoured markdown, BBCode subset, or both.
* Presence features let site members know when other users are online, offline or banned. Individual users have setting to hide their activity from non-admins.
* Complete moderation toolset allowing admin-approved moderators to edit, move, hide, approve, delete or close user posted content. This also includes option to delete or block user accounts or avatars.
* Ban system allows you to ban existing users as well as forbid certain user names, e-mails or IP addresses from registering accounts.
* Permission system allowing you to control which features are available to users based on their rank, roles or category they are in.
* Private threads feature allowing users to create threads visible only to them and those they've invited. 
* Rich polls  system, allowing polls with public and private voters, single and multiple choices as well as ones that allow vote change or limit voting tp limited period of time.
* Post attachments complete thumbnailing and gif's animation removal.
* Posts edits log allowing you to see how user messages used to look in past as well as revert function protecting you from malignant users emptying their posts contents.
* Moderation queue for users and categories allowing you to moderate content before it becomes visible to other members of the community.
* Custom theme developed over bootstrap.

Even more features will follow in future releases:

* Admin-manageable custom profile fields letting site admins to define custom fields for users to fill in without need to write any code.
* Content reporting for users to report offensive content.
* Forum-wide JS routing further reducing navigation times.
* Notifications for users to notice content and events of concern faster.
* Post accurate read tracker that lets moderators spot unapproved replies and non-moderators spot approved posts.
* Warning system for easy tracking users history of infractions and offenses.
* WYSIWYM content editor for even easier post formatting.

If you are looking into using Misago to run live forum, you are absolutely invited to, but please keep in mind that Misago is relatively immature software that may contain serious bugs or issues as well as quirks and lackings thay may take time to resolve, despite best efforts. 


Development
===========

To start Misago site locally, first setup and activate virtual environment for it and then fire following commands::

    python setup.py install
    misago-start.py testforum

This will install Misago and its dependencies in your virtual environment and will make pre-configured Misago site for you named ``testforum``::

    testforum
      + avatar_store
      + media
      + testforum
        * __init__.py
        * settings.py
        * urls.py
        * wsgi.py
      + static
      + theme
      + cron.txt
      + manage.py

Now  edit ``settings.py`` file in your editor of choice in order to set up basic settings like database connection, default timezone or interface language.

Next, initialize database by using migrate commands provided by ``manage.py`` admin utility that you'll find in directory up one level from where ``settings.py`` is::

    python manage.py migrate

Then, call ``createsuperuser`` command to create super admin in database::

    python manage.py createsuperuser

Finally start development server using ``runserver`` command::

    python manage.py runserver

If nothing is wrong with your setup, Django developer server will start, enabling you to visit ``127.0.0.1:8000`` in your browser and see the forum index. You should now be able to sign in to user account that you have created ealier.

You will likely want to customize your site via changing settings and creating categories. You can do this with Admin Control Panel available under ``127.0.0.1:8000/admincp/`` url.


Frontend
--------

With exception of Admin Panel, Misago frontend relies heavily on React.js components backed by Django API. This application relies on custom Gulp.js-based toolkit for development. As of current, Misago's ``gulpfile.js`` defines following tasks:

* **build** does production build of Misago's assets, concating and minifying javascripts, css and images, as well as moving them to misago/static directory
* **watch** does quick build for assets (concat assets into single files, compile less, deploy to misago/static but don't minify/optimize) as well as runs re-build when less/js changes
* **watchstyle** does quick build of less files, and re-builds them when they change
* **test** runs Mocha.js tests suite for Misago's javascript

To start work on custom frontend for Misago, fork and install it locally to have development forum setup. You can now develop custom theme by modifing assets in ``frontend`` directory, however special care should be taken when changing source javascripts.

Misago defines template that allows you to include custom html and js code before Misago's JavaScript app is ran, named **scripts.html**.


Bug reports, features and feedback
==================================

If you have found bug, please report it on `issue tracker <https://github.com/rafalp/Misago/issues>`_.

For feature or support requests as well as general feedback please use `official forum <http://misago-project.org>`_ instead. Your feedback means much to the project so please do share your thoughts!

There's also Gitter for those looking for intant-messaging approach for discussing Misago development.


Contributing
============

If you have corrected spelling, wrote new tests or fixed a bug, feel free to open pull request.

Many issues are open for takers. If you've found one you feel you could take care of, please announce your intent in issue discussion before you start working. That way situations when more than one person works on solving same issue can be avoided.


Authors
=======

**Rafał Pitoń**

* http://rpiton.com
* http://github.com/rafalp
* https://twitter.com/RafalPiton


English sentences used within ``misago.faker.phrases`` were extracted from `National Aeronautics and Space Administration Solar System Exploration Portal <http://solarsystem.nasa.gov/planets/>`_ and are not copyrighted as per `Media and content usage guidelines <https://www.nasa.gov/multimedia/guidelines/index.html>`_.


Copyright and license
=====================

**Misago** - Copyright © 2016 `Rafał Pitoń <http://github.com/ralfp>`_
This program comes with ABSOLUTELY NO WARRANTY.

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.rst
