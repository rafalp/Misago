Misago
======

Misago is internet forum application written in Python and using Django as its foundation.
Visit project homepage for discussion and demo: <http://misago-project.org>


The Tao AKA Mission Statement
-----------------------------

I want software focused on enabling smooth flow of information between forum members. I dont want to build "Facebook CMS" that contains lots of extra functionality like user galleries, blogs or user walls. Posting and replying in threads is only focus of Misago with additional features implemented to improve forum users and staff experience.

Secondary goal is making Misago a viable foundation for building and maintaining long-term discussion forums for administrators. Misago trades "casual admin" friendlyness for advanced features aimed for use by web developers looking for tool to build forums for their site.

Finally while Misago is build using Django, its not "Django application" and it wont integrate with existing Django projects. This is result of design decision to use custom users/session/auth/permissions functionality instead of Django native applications - however in future Misago will provide web API allowing you to add Misago-powered features to your website.


Dependencies
------------

* [Django](http://djangoproject.com)
* [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)
* [Django-MPTT](https://github.com/django-mptt/django-mptt)
* [Coffin](https://github.com/coffin/coffin)
* [Jinja2](https://github.com/mitsuhiko/jinja2)
* [Markdown](http://pypi.python.org/pypi/Markdown)
* [path](http://pypi.python.org/pypi/path.py)
* [Pillow](http://pypi.python.org/pypi/Pillow/)
* [pyTZ](http://pypi.python.org/pypi/pytz/2012h)
* [reCAPTCHA](http://pypi.python.org/pypi/recaptcha-client)
* [South](http://south.aeracode.org)
* [Unidecode](http://pypi.python.org/pypi/Unidecode)


Installation
------------

Misago comes with "deployment" python module that contains empty Misago configuration and default Django WSGI container for you to use in your deployments.

After you set low-level configuration of Misago, fire following commands on manage.py:

* __startmisago__ - creates DB structure for Misago and populates it with default data
* __adduser Admin admin@example.com password --admin__ - this will create first admin user

Misago stands on shoulders of Django and Django documentation covers deployment of apps extensively:
https://docs.djangoproject.com/en/dev/howto/deployment/

Don't forget to set up maintenance cronjobs to keep your database clean, look into cront.txt file to see what crons to set up.

While Misago will run without cache set up, you are stronly encouraged to set one up for it.

### WARNING!

Misago is not production ready! Don't ever use it in anything thats anywhere close to production enviroment!


Updating
--------

You can use **updatemisago** command to update your forums database to latest version.


Contributing
------------

Misago is open source project. You are free to submit pull requests against master branch, but I request all interested in contributing to project to register on project forums and participate in [development discussion](http://misago-project.org/category/development-discussion-17/).

Finally, you can participate in discussion on [project forums](http://misago-project.org). Your feedback means much for project, don't keep it to yourself!


Authors
-------

**Rafał Pitoń**

+ http://rpiton.com
+ http://github.com/ralfp
+ https://twitter.com/RafalPiton


Copyright and license
---------------------

Misago  Copyright (C) 2012  Rafał Pitoń
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.

For complete license, see LICENSE.txt