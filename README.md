Misago
======

[![Test Coverage](https://coveralls.io/repos/github/rafalp/Misago/badge.svg?branch=master)](https://coveralls.io/github/rafalp/Misago?branch=master) ![Works on Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg) [![Community Chat](https://img.shields.io/badge/chat-on_discord-7289da.svg)](https://discord.gg/fwvrZgB)


**Development Status:** 🍌 [Bananas](https://en.wikipedia.org/wiki/Perpetual_beta) 🍌

Misago aims to be complete, featured and modern forum solution that has no fear to say 'NO' to common and outdated opinions about how forum software should be made and what it should do.

* **Homepage:** http://misago-project.org/
* **Documentation:** https://misago.gitbook.io/docs/
* **Code & BugTracker:** https://github.com/rafalp/Misago/


Screenshots
-----------

[![Forum index](https://user-images.githubusercontent.com/750553/212570745-fff596f8-ff7d-45f2-a7c2-505e56d80a04.png)](https://misago-project.org)

[![Thread view](https://user-images.githubusercontent.com/750553/212570742-52fa8c2c-a86e-4dd4-84b2-933ed7db41d3.png)](https://misago-project.org)


Production use
--------------

Misago implements all features considered "must have" on live internet forum:

* Your users may register accounts, set avatars, change options and edit their profiles. They have option to reset forgotten password.
* Sign in with Facebook, Google, Github, Steam, Blizzard.net or any other over 50 supported OAuth providers.
* Site admins may require users to confirm validity of their e-mail addresses via e-mail sent activation link, or limit user account activation to administrator action. They can use custom Q&A challenge, ReCAPTCHA, Stop Forum Spam or IP's blacklist to combat spam registrations. Pletora of settings are available to control user account behavior, like username lengths or avatar restrictions.
* Create categories together with unlimited number and depth of subcategories.
* Write messages using either GitHub flavoured markdown, BBCode subset, or both.
* Presence features let site members know when other users are online, offline or banned. Individual users have setting to hide their activity from non-admins.
* Complete moderation toolset allowing admin-approved moderators to edit, move, hide, approve, delete or close user posted content. This also includes option to delete or block user accounts or avatars.
* Ban system allows you to ban existing users as well as forbid certain user names, e-mails or IP addresses from registering accounts.
* Permission system allowing you to control which features are available to users based on their rank, roles or category they are in.
* Post accurate read tracker that lets your users spot threads with new posts as well as let moderators spot unapproved replies and non-moderators spot approved posts.
* Private threads feature allowing users to create threads visible only to them and those they've invited. 
* Python-based profile fields framework letting site owners to define custom fields for users to fill in complete with powerful customization options for custom requirements, display or validation logic.
* Rich polls system, allowing polls with public and private voters, single and multiple choices as well as ones that allow vote change or limit voting tp limited period of time.
* Post attachments complete thumbnailing and gif's animation removal.
* Mark post in question thread as best answer, bringing basic Q&A functionality.
* Posts edits log allowing you to see how user messages used to look in past as well as revert function protecting you from malignant users emptying their posts contents.
* Moderation queue for users and categories allowing you to moderate content before it becomes visible to other members of the community.
* Custom theme developed with bootstrap.
* Features and settings for achieving GDPR compliance.
* Integrate forum with your site using implemented OAuth2 client and JSON API.

Even more features will follow in future releases:

* Forum-wide JS routing further reducing navigation times.
* Replacing current API with GraphQL API for easier integrations and extending.
* Plugin system to extend core package with new features.
* WYSIWYM content editor for even easier post formatting.
* Ranking system for forum search results based on post links, likes, author and thread importance.


Development
-----------

Preferred way to run Misago development instances on your machine is with [Docker](https://www.docker.com/community-edition#/download), which makes it easy to spin up arbitrary number of instances running different code with separate databases and dependencies besides each other.

To start, clone the repository and run `./dev init` command in your terminal. This will build necessary docker containers, install python dependencies and initialize the database. After command does its magic, you will be able to start development server using the `docker compose up` command.

After development server starts, visit the <http://127.0.0.1:8000/> in your browser to see your Misago installation.

Admin Control Panel is available under the <http://127.0.0.1:8000/admincp/> address. To log in to it use `Admin` username and `password` password.

The `./dev` utility implements other features besides the `init`. Run it without any arguments to get the list of available actions.


### Running Misago in development without `dev`

You may skip `./dev init` and setup dev instance manually, running those commands:

1. `docker compose build`: builds docker containers
2. `docker compose run --rm misago python manage.py migrate`: runs migrations
3. `docker compose run --rm misago python manage.py createsuperuser`: creates admin user
4. `docker compose up`: starts dev server


### Frontend

With exception of Admin Panel, Misago frontend relies heavily on React.js components backed by Django API. This application uses webpack for building.

Currently Misago's `package.json` defines following tasks:

* `npm run build`: does production build of Misago's assets, bundling and minifying JavaScript, CSS and images, as well as moving them to the `misago/static/misago` directory.
* `npm run start`: does quick build for assets:bundling, compiling less, deployment to `misago/static/misago`. Doesn't minify/optimize. Runs re-build when less/js file changes.
* `npm run prettier`: formats code with prettier.
* `npm run eslint`: lints the code with eslint.

To start work on custom frontend for Misago, fork and install it locally to have development forum setup. You can now develop custom theme by modifying assets in `frontend` directory, however special care should be taken when changing source JavaScript files as no test suite for those exists.

Misago defines template that allows you to include custom html and JavaScript code before Misago's JavaScript app is ran, named `scripts.html`.


### Admin

Admin assets are stored in `misago-admin` directory and deployed to `misago/static/misago/admin` directory on build.

To work on admin's JavaScript or CSS, `cd` to `misago-admin` and install dependencies with `npm install`. Now you can use following actions:

* `npm run build`: does production build of assets, bundling and minifying JavaScript and CSS files.
* `npm run dev`: does quick build for JavaScript and CSS assets, only bundling but not minifying. Also does a rebuild when one of the files changes.


### Emails

Misago uses [Mailpit](https://github.com/axllent/mailpit) to capture emails sent from the development instance.

To browse those emails, visit the <http://127.0.0.1:8025> in your browser for the web interface.


### Note for Windows users

If you are using Windows, you may see the following error during installation:

```
 => ERROR [misago 8/8] RUN ./dev bootstrap_plugins
------
 > [misago 8/8] RUN ./dev bootstrap_plugins:
0.385 /bin/sh: 1: ./dev: not found
------
failed to solve: process "/bin/sh -c ./dev bootstrap_plugins" did not complete successfully: exit code: 127
```

This error is caused by the `dev` file having its line endings converted from Unix format (`LF`) to Windows (`CRLF`) by git when you cloned the repository. To fix this, disable the automatic conversion of line endings in your git configuration and then clone the repository again.


Providing feedback and contributing
-----------------------------------

If you have found a bug, please report it either on the [issue tracker](https://github.com/rafalp/Misago/issues) or on the [project's forums](hhttps://misago-project.org/c/bug-reports/29/).

If you want to contribute to project, please see the [contributing](./CONTRIBUTING.md) document.

For feature or support requests as well as general feedback please use the [official forums](http://misago-project.org). Your feedback means much to the project so please do share your thoughts!

There's also a [Discord server](https://discord.gg/fwvrZgB) for those looking for instant-messaging approach for getting in touch with Misago devs and users.


Authors
-------

**Rafał Pitoń** and ❤️ [contributors](https://github.com/rafalp/misago/graphs/contributors).

* http://rpiton.com
* http://github.com/rafalp
* https://twitter.com/RafalPiton


English sentences used within `misago.faker.phrases` were extracted from [National Aeronautics and Space Administration Solar System Exploration Portal](http://solarsystem.nasa.gov/planets/) and are not copyrighted as per [Media and content usage guidelines](https://www.nasa.gov/multimedia/guidelines/index.html).


Copyright and license
---------------------

**Misago** - Copyright © 2023 [Rafał Pitoń](http://github.com/rafalp)
This program comes with ABSOLUTELY NO WARRANTY.

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.rst
