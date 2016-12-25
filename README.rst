======
Misago
======

.. image:: https://travis-ci.org/rafalp/Misago.png?branch=master
   :target: https://travis-ci.org/rafalp/Misago
   :alt: Tests Result

.. image:: https://coveralls.io/repos/rafalp/Misago/badge.png?branch=master
   :target: https://coveralls.io/r/rafalp/Misago?branch=master
   :alt: Code Coverage

.. image:: https://badges.gitter.im/Misago/Misago.svg
   :target: https://gitter.im/Misago/Misago?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
   :alt: Development Chat


**Development Status: Pre-Alpha**

Misago aims to be complete, featured and modern forum solution that has no fear to say 'NO' to common and outdated opinions about how forum software should be made and what it should do.

If you can run Python apps on your hosting and you are looking for modern solution using latest paradigms in web development, or you are Django developer and forum is going to be core component of your next project then Misago is option for you.

* **Homepage:** http://misago-project.org/
* **Documentation:** http://misago.readthedocs.org/en/latest/
* **Code & BugTracker:** https://github.com/rafalp/Misago/


Don't use this branch in production!
====================================

This branch contains in-development code of next major Misago release, 0.6. **It's not feature-complete.** If you are looking at running "real" forum on Misago, please use latest 0.5 release instead.

**There is no update path for pre-release 0.6 installations!** If you run your site off codebase pulled straight from git branch instead of release or pypi install, you'll won't be able to do smooth update via ``python manage.py migrate``.


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


English sentences used within ``misago.faker.phrases`` were extracted from `National Aeronautics and Space Administration Solar System Exploration Portal<http://solarsystem.nasa.gov/planets/>`_ and are not copyrighted as per `Media and content usage guidelines <https://www.nasa.gov/multimedia/guidelines/index.html>`_.


Copyright and license
=====================

**Misago** - Copyright © 2016 `Rafał Pitoń <http://github.com/ralfp>`_
This program comes with ABSOLUTELY NO WARRANTY.

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.rst
