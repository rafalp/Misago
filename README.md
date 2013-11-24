# Misago [![Build Status](https://travis-ci.org/rafalp/Misago.png?branch=master)](https://travis-ci.org/rafalp/Misago)

Misago is an internet forum application written in Python and using Django as its foundation. Visit the project homepage for discussion and a live demo: <http://misago-project.org>

> #### Notice!
>
> __Misago is not yet production ready! Don't ever use it in anything thats anywhere close to a production enviroment!__

The Tao AKA Mission Statement
-----------------------------

My vision is software focused on enabling a smooth flow of information between forum members. I don't want to build a "Facebook CMS" that contains lots of extra functionality like user galleries, blogs or user walls. Posting and replying in threads is the only focus of Misago with additional features implemented to improve the experience for forum users and staff.

The secondary goal is making Misago a viable foundation for building and maintaining long-term discussion forums for administrators. Misago trades "casual admin" friendliness for advanced features aimed for use by web developers looking for a tool to build forums for their site.

Finally, while Misago is built using Django, it's not a "Django application" and it won't integrate with existing Django projects. This is the result of a design decision to use custom users/session/auth/permissions functionality instead of native Django applications - however, in the future Misago will provide a web API allowing you to add Misago-powered features to your website and/or application.


Dependencies
------------

* [Django](http://djangoproject.com)
* [Django Debug Toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)
* [Django-MPTT](https://github.com/django-mptt/django-mptt)
* [Coffin](https://github.com/coffin/coffin)
* [Django Haystack 2](http://haystacksearch.org/)
* [Jinja2](https://github.com/mitsuhiko/jinja2)
* [Markdown](http://pypi.python.org/pypi/Markdown)
* [path](http://pypi.python.org/pypi/path.py)
* [Pillow](http://pypi.python.org/pypi/Pillow/)
* [pyTZ](http://pypi.python.org/pypi/pytz/2012h)
* [reCAPTCHA-client](http://pypi.python.org/pypi/recaptcha-client)
* [South](http://south.aeracode.org)
* [Unidecode](http://pypi.python.org/pypi/Unidecode)

You will also need search engine to provide search functionality. If you don't have one, [Whoosh 2](https://pypi.python.org/pypi/Whoosh/) is pure Python search engine that's easy to setup.

Installation
------------

### Vagrant setup

Misago comes with a Puppet-provisioned Vagrant-setup that you can use to get Misago up and running in a development environment with just a couple of commands. The first thing you want to do is clone Misago:

```sh
git clone git://github.com/rafalp/Misago.git
```

The next step is to boot up the VM and provision it:

```sh
cd Misago && vagrant up
```

You might want to grab a coffee while Puppet works its magic as the process usually takes ~5 minutes. When the VM is booted and Puppet is done provisioning, ssh into the VM and start the Django development server:

```sh
vagrant ssh
cd /vagrant
sudo python manage.py runserver 192.168.33.10:80 # Private network address as per the Vagrant config
```

Now navigate to [192.168.33.10](http://192.168.33.10) in your browser of choice to find your forums all set up and ready for testing and development. Puppet will have taken care of bootstrapping your Misago installation with a database, some dummy content and an admin user with the following credentials:

__Username__: Admin  
__Email__: admin@example.com  
__Password__: password

Be aware that the defualt configuration doesn't contain anything besides the bare-minimum for Misago to run - this meaning that things like an SMTP server will have to added manually if you wish to test Misago's email features.

### Manual setup

If you'd like to test Misago in a more production-ish environment instead of the Vagrant development environment, you're free to do so. The very first thing that needs to be done is ensure you have all the dependencies installed, most of which can be installed through `pip`.

Misago comes with the "deployment" Python module that contains an empty Misago configuration and a default Django WSGI container for you to use in your deployments. On top of this you can then add an HTTP and/or HTTP Proxy server - Gunicorn and Nginx would be a good mix.

After you set low-level configuration of Misago ([`deployment/settings.py`](deployment/settings.py)), fire the following commands on manage.py through the Python executable:

* `startmisago [--quiet]`  
  Creates the DB structure for Misago and populates it with default data
* `adduser [--admin] <username> <email> <password>`  
  Adds a new user to the database.  
  Make sure to do something like `adduser Admin admin@example.com password --admin` to add an admin user when you first setup your forums.

Misago stands on shoulders of Django and Django documentation covers deployment of apps extensively: https://docs.djangoproject.com/en/dev/howto/deployment/

Don't forget to set up maintenance cronjobs to keep your database clean. You can look into [cron.txt](cron.txt) file to see what cronjobs to set up.

While Misago will run without a cache set up, you are strongly encouraged to set one up for it. Even if you choose not to run one, you will still need to set a default one (such as dummy caching).


Updating
--------

You can use the `updatemisago` command to update your forums database to latest version _unless_ you are updating from `0.1` which is incompatibile with `0.2` and later releases.

Support for migrations from `0.1` has been dropped with `0.3` release.


Contributing
------------

Misago is an open source project. You are free to submit pull requests against the master branch and use the issue tracker to report bugs as well as propose improvements and/or new features.

Finally, you can participate in discussion on the [project forums](http://misago-project.org). Your feedback means much to the project so please do share your thoughts!


Authors
-------

**Rafał Pitoń**

+ http://rpiton.com
+ http://github.com/ralfp
+ https://twitter.com/RafalPiton


Copyright and license
---------------------

> __Misago__ - Copyright © 2013 [Rafał Pitoń](http://github.com/ralfp)  
> This program comes with ABSOLUTELY NO WARRANTY.  
> This is free software and you are welcome to redistribute it under the conditions described in the license.
>
> For the complete license, refer to [LICENSE.md](LICENSE.md)
