Misago
======

Misago is an internet forum application written in Python and using Django as its foundation.
Visit project homepage for discussion and demo: <http://misago-project.org>


The Tao AKA Mission Statement
-----------------------------

I want software focused on enabling smooth flow of information between forum members. I don't want to build a "Facebook CMS" that contains lots of extra functionality like user galleries, blogs or user walls. Posting and replying in threads is the only focus of Misago with additional features implemented to improve forum users and staff experience.

Secondary goal is making Misago a viable foundation for building and maintaining long-term discussion forums for administrators. Misago trades "casual admin" friendliness for advanced features aimed for use by web developers looking for a tool to build forums for their site.

Finally while Misago is built using Django, it's not a "Django application" and it won't integrate with existing Django projects. This is the result of design decision to use custom users/session/auth/permissions functionality instead of Django native applications - however in the future Misago will provide a web API allowing you to add Misago-powered features to your website.


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
* [reCAPTCHA-client](http://pypi.python.org/pypi/recaptcha-client)
* [South](http://south.aeracode.org)
* [Unidecode](http://pypi.python.org/pypi/Unidecode)


Installation
------------

The very first thing that needs to be done is ensure you have all the dependencies installed. Most can be installed through `pip`.

Misago comes with the "deployment" Python module that contains empty Misago configuration and default Django WSGI container for you to use in your deployments.

After you set low-level configuration of Misago (`settings/settings.py`), fire the following commands on manage.py through the Python executable:

* __initmisago__ - creates DB structure for Misago and populates it with default data
* __adduser__ Admin admin@example.com password --admin__ - this will create first admin user

Misago stands on shoulders of Django and Django documentation covers deployment of apps extensively:
https://docs.djangoproject.com/en/dev/howto/deployment/

Don't forget to set up maintenance cronjobs to keep your database clean, look into cront.txt file to see what crons to set up.

While Misago will run without cache set up, you are strongly encouraged to set one up for it. Even if you choose not to run one, you will still need to set a default one (such as dummy caching).

### WARNING!

Misago is not production ready! Don't ever use it in anything thats anywhere close to production enviroment!


Contributing
------------

Misago is open source project. You are free to submit pull requests against master branch, and use issues system to report bugs, propose improvements and new features.

Finally, you can participate in discussion on [project forums](http://misago-project.org). Your feedback means much more for the project, don't keep it to yourself!


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

For the complete license, see LICENSE.txt