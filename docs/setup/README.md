Setup and maintenance
=====================

Misago is Python and Django application which means system requirements as well as setup process and way maintenace tasks are performed may appear confusing and suprising to administrators that have no experience outside of running PHP solutions.


## Installing Misago

Misago installation is three step process. First you compare your server's specification to check if it will be able to run Misago. Next you setup Misago and all extra services required for it to function like e-mails, database and automatic maintenance tasks. Finally you get your site running and accessible for your users.


### Requirements

Before you start make sure your hosting provider grants you:

- SSH access to the server
- Python 2.7, 3.4, 3.5 or 3.6
- SetupTools >= 8.0
- PostgreSQL >= 9.4 with access to superuser and GIN extension
- At least 128 megabytes of free memory for Misago's processes
- HTTP server that supports WSGI applications (like NGINX with UWSGI or Apache2 with mod_wsgi)
- Crontab

This isn't an issue on VPS or dedicated servers, but availability of shared servers that meet those requirements differs wildly depending on your location.

Speaking of shared servers, ability to download, compile and run software from the internet may be needed, but different ISP's have different approaches to this. Some options come with all dependencies preinstalled, others let you install them yourself and others require you to mail them every time you need something installed. Generally you should avoid offers coming from the last group because this turns running Python apps into a chore.


#### About the `'install_requires' must be a string or list of strings containing valid project/version requirement specifiers` error during installation

This error is caused by Misago being installed using setuptools older than 8.0 release, which was first to introduce support for [PEP 440](https://www.python.org/dev/peps/pep-0440/), which defines version requirments used in Misago's requirements.txt.


### Setup

To install Misago setup and activate virtual environment for your site, then fire the following command:

    pip install misago

This will install Misago in your virtual environment and make `misago-start.py` script available for you to use to create a pre-configured Misago site.

Now decide on your site's module name. This name will be used for python module that will contain your configuration files. This means it should be only latin lowercase letters and (optionally) digits or underscore sign ("_"). Good idea is to use your domain name as source for project namespace, for example turning "misago-forum.org" into "misagoforumorg".

Once you've decided on your name, create your site configuration module. In this example we assume your site will be named "misagoforumorg":

    misago-start.py misagoforumorg

This will create the directory "misagoforumorg" in your working directory. Inside you will find the following items:

* `manage.py` - Script that you can use to run administrative commands Misago provides as well as access its python shell which is usefull for quick and dirty administration work.
* `cron.txt` - Contains example crontab configuration for automating maintenance tasks on your site.
* `avatargallery` - Directory that contains example avatar gallery you may load using `manage.py` script to run `loadavatargallery` task that will load it into avatar gallery.
* `media` - Directory for user uploaded files.
* `misagoforumorg` - Python module with configuration files for your site.
* `static` - Directory for static assets like css, js or images.
* `theme` - Directory for overriding default assets with your own ones.

We will get to `misagoforumorg` in a minute, but before that lets spend few more moments in our current location.

This directory has special purpose. It serves as "container" for your customizations for Misago. If you want to install an extension or plugin that has no `setup.py` of its own or use custom styles or templates on your site, you will put them there, making them easily accessible for your Misago installation.

Let's go deeper. Change your current directory to "misagoforumorg". By default this directory will contain four files: 
 
* `__init__.py` - Special file that tells python this directory is python package
* `settings.py` - Contains all low-level settings of your site
* `urls.py` - Tells your forum about links on your site
* `wsgi.py` - Special file servers use to understand and talk with your application. Unless you are building the entire site around your forum, you can ignore `urls.py`.

Open `settings.py` in your code editor of choice and take a look at the values listed here. Each value is accompanied by commentary explaining its purpose. You'll need to setup the database connection before next step.

Move back to directory with manage.py and use it to initialize Misago database by firing migrate:

    python manage.py migrate

Next, call createsuperuser command to create a super admin in database:

    python manage.py createsuperuser

Finally, start development server using the "runserver" command:

    python manage.py runserver

If server starts, you should be able to visit `http://127.0.0.1:8000` in your browser and see forum index, however as work on the project is underway revisions may frequently introduce changes that will break runserver.


#### About the `could not open extension control file` error during database migration

If you run into any of following errors during migration:

    django.db.utils.OperationalError: could not open extension control file "/usr/share/postgresql/9.4/extension/btree_gin.control": No such file or directory
    django.db.utils.OperationalError: could not open extension control file "/usr/share/postgresql/9.4/extension/hstore.control": No such file or directory

This means you'll need to install the `postgresql-contrib` package that includes extensions for PostgreSQL:

    sudo apt-get install postgresql-contrib


#### About the `django.db.utils.ProgrammingError: permission denied to create extension` errors during database migration

Misago relies on two PostgreSQL extensions for some of its features: the `btree_gin` and `hstore` extensions. If during migration command you get error that looks like one of those:

    django.db.utils.ProgrammingError: permission denied to create extension "btree_gin"
    django.db.utils.ProgrammingError: permission denied to create extension "hstore"

This means you'll need to elevate your database user to superuser level for duration of migration.

To grant your database user super user privileges for duration of the installation, you may follow those steps:

    # switch to postgresql user and start psql tool
    sudo -u postgres psql postgres

    # make your database user the superuser
    alter role user_name superuser;

    # after installation is complete run below query in the psql
    # to remove super user privileges from your database user
    alter role user_name nosuperuser;


### Deployment

Deployment is a process in which you get your site running and reachable by your users.

Misago is de facto Django with extra features added. This means deployment of Misago should be largery same to deployment of other Django-based software. Django documentation covers supported [deployment methods](https://docs.djangoproject.com/en/{{ book.django_version }}/howto/deployment/wsgi/) as well provides [checklist](https://docs.djangoproject.com/en/{{ book.django_version }}/howto/deployment/checklist/) of things that **need** to be done on deployment.

If you need an example, UWSGI project's documentation has a tutorial on configuring NGINX with UWSGI to run [django applications](http://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html).


##### Note about shared hostings and Platform as a Service providers

While on dedicated and VPS serves the deployment method depends largery on your preference, shared servers may differ greatly when it comes to the way Django should be deployed as well as with services such as media and staticfiles storage or cache engines. If that's the case, make sure you consult your ISP documentation and/or ask its support for details about deployment methods available.


### Securing `MEDIA_ROOT`

By default Misago uses the `FileSystemStorage` strategy that stores user-uploaded files in your site's `media` directory. You need to make sure that you have disabled indexing/listing of this directory contents in your HTTP server's settings, or your user-uploaded files will be easily discoverable from internet. This is especially important because Misago has no special protection system in place for uploaded files.


### Setting up maintenance tasks

Misago relies on periodically ran maintenance tasks for some features to run performantly or work at all. For example, there is task that removes expired entries from data used by read tracker, thus keeping it small and performant. There's also an task that populates active posters list on Misago's users page with current data. Without it, that list will be empty.

When new forum setup is created using `misago-start.py`, example cron file named `cron.txt` is created. This file may differ between versions, but will look similiar to this:

    # this is example crontab configuration
    # you'll likely need to change it to use
    # valid python version or paths to manage.py

    15 0 * * * python manage.py prunecategories
    25 0 * * * python manage.py buildactivepostersranking
    25 0 * * * python manage.py clearattachments
    25 0 * * * python manage.py clearreadtracker
    25 0 * * * python manage.py clearsessions
    25 0 * * * python manage.py invalidatebans

Depending on your python and virtual env setup, you'll need to customize it before it works. Here's example config that was edited to activate venv before running the commands:

    # this is example crontab configuration
    # you'll likely need to change it to use
    # valid python version or paths to manage.py

    10 0 * * * cd /home/myforumorg/ && venv/bin/python manage.py prunecategories
    35 0 * * * cd /home/myforumorg/ && venv/bin/python manage.py buildactivepostersranking
    35 0 * * * cd /home/myforumorg/ && venv/bin/python manage.py clearattachments
    35 0 * * * cd /home/myforumorg/ && venv/bin/python manage.py clearreadtracker
    35 0 * * * cd /home/myforumorg/ && venv/bin/python manage.py clearsessions
    35 0 * * * cd /home/myforumorg/ && venv/bin/python manage.py invalidatebans
    0 3 * * * cd /home/myforumorg/ && venv/bin/python manage.py backupsite