======
Misago
======

.. image:: https://travis-ci.org/rafalp/Misago.png?branch=master
  :target: https://travis-ci.org/rafalp/Misago

.. image:: https://coveralls.io/repos/rafalp/Misago/badge.png?branch=master
  :target: https://coveralls.io/r/rafalp/Misago?branch=master

.. image:: https://ci.appveyor.com/api/projects/status/3v4ewukx2kvjpvpn/branch/master
  :target: https://ci.appveyor.com/project/rafalp/misago/branch/master

**Development Status: Pre-Alpha**

Misago aims to be complete, featured and modern forum solution that has no fear to say 'NO' to common and outdated opinions about how forum software should be made and what it should do.

If you can run Python apps on your hosting and you are looking for modern solution using latest paradigms in web development, or you are Django developer and forum is going to be core component of your next project then Misago is option for you.

* **Homepage:** http://misago-project.org/
* **Documentation:** http://misago.readthedocs.org/en/latest/
* **Code & BugTracker:** https://github.com/rafalp/Misago/


Don't use this branch in production!
====================================

This branch contains in-development code of next major Misago release, 0.6. **It's not feature-complete.** If you are looking at running "real" forum on Misago, please use latest 0.5 release instead.

**There is no update path for 0.6 installations!**


Development
===========


To start Misago site locally, first setup and activate virtual environment for it and then fire following commands::

    python setup.py install
    misago-start.py testforum

This will install Misago in your virtual environment and will make pre-configured Misago site for you named "testforum". It will also expose "requirements.txt" for you to use to install Misago dependencies::

    pip install -r requirements.txt

Now cd to "testforum" and edit "settings.py" file in your editor of choice in order to set up basic settings like database connection, default timezone or interface language.

Next, initialize database by using migrate commands provided by manage.py admin utility::

    cd testforum
    python manage.py migrate

Then, call "createsuperuser" command to create super admin in database::

    python manage.py createsuperuser

Finally start development server using "runserver" command::

    python manage.py runserver


If nothing is wrong with your setup, Django developer server will start, enabling you to visit 127.0.0.1:8000 in your browser and see the (incomplete) forum index.


Frontend
--------

With exception of Admin Panel, Misago frontend is powered by Mithril.js application backed by Django API. This application relies on custom Node.js-based toolkit for development.


Bug reports, features and feedback
==================================

If you have found bug, please report it on `issue tracker <https://github.com/rafalp/Misago/issues>`_.

For feature or support requests as well as general feedback please use `official forum <http://misago-project.org>`_ instead. Your feedback means much to the project so please do share your thoughts!


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


Copyright and license
=====================

**Misago** - Copyright © 2014 `Rafał Pitoń <http://github.com/ralfp>`_
This program comes with ABSOLUTELY NO WARRANTY.

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.rst
