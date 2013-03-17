Refactored Code Layout
======================

Directory Tree
--------------

```
misago/                        App root structure
+-admin/                       Admin apps
+-shared/                      Shared (Admin/Front) apps
+-fixtures/                    Starting data
  +-basicsettings.py           "Basic Settings" group fixture
  +-captchasettings.py         "Captcha Settings" group fixture
  +-usersmonitor.py            Users Monitor fixture
+-forms/                     Misago forms
  +-fields.py                Custom fields
  +-forms.py                 Custom form base class
  +-layouts.py               Forums layouts (wrapper around Django forms that enables templating)
  +-widgets.py               Custom widgets
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
+-cookiejar.py                 CookieJar allows for easy setting and removing cookies without direct access to response object
+-dbsettings.py                DB based settings controller
+-monitor.py                   Monitor controller that tracks forum stats
+-settingsbase.py              Base configuration
+-signals.py                   Misago's signals
+-urls.py                      Default urls
+-validators.py                Misago's validators
+-stopwatch.py                 Stopwatch controller for measuring request processing time
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
* Moved Ban model to models package.


Bruteforce
----------
* Moved SignInAttempt model to models package.


Captcha
-------
* Turned into module and moved to core.forms package


CookieJar
---------
* Moved controller to core package.
* Moved middleware to middleware package.


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


ForumRoles
----------
* Moved ForumRole model to models package.


Forums
------
* Moved Forum model to models package.


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
* Moved Newsletter model to models package.


Profiles
--------


Prune
-----
* Renamed "Policy" model to "PruningPolicy" and moved to models package.


Ranks
-----
* Moved Rank model to models package.


Readstracker
------------
* Renamed "ForumRecord" model to "ForumRead" and moved to models package.
* Renamed "ThreadRecord" model to "ThreadRead" and moved to models package.


Register
--------


ResetPswd
---------


Roles
-----
* Moved Role model to models package.


Search
------


Sessions
--------
* Moved Session model to models package.


Settings
--------
* Moved controller to core package.
* Moved context processor to main context processor.
* Moved fixture utils to fixtures.py module in utils package.
* Moved middleware to middleware package.
* Moved Setting model to models package.
* Renamed "type" attribute on Setting model to "normalizes_to".
* Renamed "input" attribute on Setting model to "field".
* Renamed model "Group" to "SettingsGroup" and moved it to models package.


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
* Moved Thread model to models package.
* Moved Post model to models package.
* Moved Karma model to models package.
* Moved Change model to models package.
* Moved Checkpoint model to models package.


Timezones
---------
* Turned into module in utils package.


ToS
---


UserCP
------
* Moved UsernameChange model to models package.


Users
-----
* Moved User model to models package.
* Moved Guest model to models package.
* Moved Crawler model to models package.


Utils
-----
* Split __init__.py module into datesformat, pagination, translation and strings modules.
* Renamed "get_random_string" function to "random_String" in strings module.


Watcher
-------
* Renamed "ThreadWatch" model to "WatchedThread" and moved to models package.