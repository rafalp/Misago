Setup and maintenance
=====================

Misago is Python and Django application which means system requirements as well as setup process and way maintenace taks are performed may appear confusing and suprising to administrators that have no experience outside of running PHP solutions.


## Installing Misago

Misago installation is three step process. First you compare your server's specification to check if will be able to run Misago. Next you setup Misago and all extra services required for it to function like e-mails, database and automatic maintenance tasks. Finally you get your site running and accessible for your users.


### Requirements

Before you start make sure your hosting provider grants you:

- SSH access to the server
- Python 2.7, 3.4, 3.5 or 3.6
- PostgreSQL >= 9.4
- At least 128 megabytes of free memory for Misago's processes
- HTTP server that supports WSGI applications (like NGINX with UWSGI or Apache2 with mod_wsgi)
- Crontab

This isn't an issue on VPS or dedicated servers, but availability of shared servers that meet those requirements differs wildly depending on your location.

Speaking of shared servers, ability to download, compile and run software from internet may be needed, but different ISP's have different approach to this. Some options come with all dependencies preinstalled, others let you install them yourself and others require you to mail them every time you need something installed. Generally you should avoid offers coming from last group because this turns running Python apps into a hore.


### Setup

To install Misago setup and activate virtual environment for your site and then fire following command:

    pip install misago --pre

This will install Misago in your virtual environment and make `misago-start.py` script available for you to use to create pre-configured Misago site.

Now decide on your site's module name. This name will be used for python module that will contain your configuration files. This means it should be only latin lowercase letters and (optionally) digits or underscore sign ("_"). Good idea is to use your domain name as source for project namespace, for example turning "misago-forum.org" into "misagoforumorg".

Once you've decided on your name, create your site configuration module. In example we assume your site will be named "misagoforumorg":

	misago-start.py misagoforumorg

This will create directory "misagoforumorg" in your working directory. Inside you will find following items:

* `manage.py` script that you can use to run administrative commands Misago provides as well as access its python shell which is usefull for quick and dirty administration work.
* `cron.txt` that contains example crontab configuration for automating maintenance tasks on your site.
* `avatargallery` directory that contains example avatar gallery you may load using `manage.py` script to run `loadavatargallery` task that will load it into avatar gallery.
* `media` directory for user uploaded files.
* `misagoforumorg` python module with configuration files for your site.
* `static` directory for static assets like css, js or images.
* `theme` directory for overriding default assets with your own ones.

We will get to `misagoforumorg` in a minute, but before that lets spend few more moments in our current location.

This directory has special purpose. It serves as "container" for your customizations for Misago. If you want to install extension or plugin that has no `setup.py` of its own or use custom styles or templates on your site, you will put them there, making them easily accessible for your Misago installation.

Let's go deeper. Change your current directory to "misagoforumorg". By default this directory will contain four files: `__init__.py`, thats special file that tells python this directory is python package, `settings.py` that contains all low-level settings of your site, `urls.py` that tells your forum about links on your site and finally `wsgi.py`, thats special file servers use to understand and talk with your application. Unless you are building entire site around your forum, you can ignore `urls.py`.

Open `settings.py` in your code editor of choice and give a look in values listed here. Each value is accompanied by commentary explaining its purpose. See if any tuning is needed, then save your changes and leave editor.


##### Note

To simplify setup process, by default `settings.py` file contains only most basic settings that are needed for your site to run, with everything else being set for you automatically at the beginning of file.


Move back to directory with manage.py and use it to initialize Misago database by firing migrate:

    python manage.py migrate

Next, call createsuperuser command to create super admin in database:

    python manage.py createsuperuser

Finally, start development server using "runserver" command:

    python manage.py runserver

If server starts, you should be able to visit `http://127.0.0.1:8000` in your browser and see forum index, however as work on project is underway revisions may frequently introduce changes that will break runserver.


### Deployment

Deployment is a process in which you get your site running and reachable by your users.

Misago is de facto Django with extra features added. This means deployment of Misago should be largery same to deployment of other Django-based solutions. Django documentation [already covers](https://docs.djangoproject.com/en/1.6/howto/deployment/) supported deployment methods, and while on dedicated and VPS options deployment method depends largery on your choice and employed software stack, shared servers may differ greatly by the way how Django should be deployed. If thats the case, make sure you consult your ISP documentation and/or ask its rep for details about supported deployment method.

If you need example, UWSGI project's documentation has tutorial on configuring NGINX with UWSGI to run [django applications](http://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html).


### Securing `MEDIA_ROOT`

By default Misago uses the `FileSystemStorage` strategy that stores user-uploaded files in your site's `media` directory. You need to make sure that you have disabled indexing/listing of this directory contents in your HTTP server's settings, or your user-uploaded files will be easily discoverable from internet. This is especially important because Misago has no special protection system in place for uploaded files.
