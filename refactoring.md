Refactored Code Layout
======================

Directory Tree
--------------

```
misago/                        App root structure
+-admin/                       Admin apps
+-shared/                      Shared (Admin/Front) apps
+-core/                        Core features
  +-forms/                     Misago forms
    +-fields.py                Custom fields
    +-forms.py                 Custom form base class
    +-layouts.py               Forums layouts (wrapper around Django forms that enables templating)
    +-widgets.py               Custom widgets
  +-monitor.py                 Monitor controller that tracks forum stats
  +-settings.py                DB based settings controller
  +-stopwatch.py               Stopwatch controller for measuring request processing time
+-fixtures/                    Starting data
  +-basicsettings.py           "Basic Settings" group fixture
  +-usersmonitor.py            Users Monitor fixture
+-front/                       Frontend apps
+-management/                  manage.py commands
+-migrations/                  South DB migrations
+-models/                      Models
+-middleware/                  Middlewares
  +-monitor.py                 Middleware that makes Monitor accessible from request.monitor
  +-settings.py                Middleware that makes DB Settings accessible from request.settings
  +-stopwatch.py               Middleware that makes Stopwatch accessible from request.stopwatch
+-templatetags/                Template tags
+-utils/                       Small helpers that are imported by models/views
  +-avatars.py                 Functions for working with avatars sizes
  +-datesformats.py            Functions for formatting dates and times
  +-fixtures.py                Fixture loaders
  +-pagination.py              Pagination helper
  +-strings.py                 Strings utilities (make slug from string, generate random string, etc. ect.)
  +-timezones.py               Generate fancy timezones list
  +-translation.py             Functions for working with translation strings
+-__init__.py                  Misago init, contains Misago version
+-context_processors.py        Misago context processors
+-settingsbase.py              Base configuration
+-urls.py                      Default urls
```


ACL
---


Activation
----------


Admin
-----


Alerts
------


Authn
-----


Banning
-------


Bruteforce
----------


Captcha
-------


Cookiejar
---------


Crawlers
--------


CSRF
----


Firewalls
---------


Forms
-----
* Moved package under core package.
* Split __init__.py into three modules.


Forumroles
----------


Forums
------


Heartbeat
---------


Markdown
--------


Messages
--------


Monitor
-------
* Moved controller to core package.
* Moved context processor to main context processor.
* Moved fixture utils to fixtures.py module in utils package.
* Moved middleware to middleware package.
* Renamed model Item to MonitorItem and moved it to models package.


Newsfeed
--------


Newsletters
-----------


Profiles
--------


Prune
-----


Ranks
-----


Readstracker
------------


Register
--------


ResetPswd
---------


Roles
-----


Search
------


Sessions
--------


Settings
--------
* Moved controller to core package.
* Moved context processor to main context processor.
* Moved fixture utils to fixtures.py module in utils package.
* Moved middleware to middleware package.
* Moved Setting model to models package.
* Renamed "type" attribute on Setting model to "normalizes_to".
* Renamed "input" attribute on Setting model to "field".
* Renamed model Group to SettingsGroup and moved it to models package.


Setup
-----
* Moved management commands to management package.
* Renamed "initdata" command to "syncfixtures".
* Moved fixture utils to fixtures.py module in utils package.
* Moved Fixture model to models package.
* Renamed "app_name" attribute on Fixture model to "name".


Stats
-----


Stopwatch
---------
* Moved controller to core package.
* Moved middleware to middleware package.
* Added "stopwatch" to template context.


Team
----


Template
--------


Themes
------


Threads
-------


Timezones
---------
* Turned into module in utils package.


ToS
---


UserCP
------


Users
-----


Utils
-----
* Split __init__.py module into datesformat, pagination, translation and strings modules.


Watcher
-------