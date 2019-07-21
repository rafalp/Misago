Misago
======

> **NOTE:** This branch contains exploration code for potential future version of Misago that is fully asynchronous and developer without Django.

[![Tests Result](https://travis-ci.org/rafalp/Misago.svg?branch=master)](https://travis-ci.org/rafalp/Misago)
[![Test Coverage](https://coveralls.io/repos/github/rafalp/Misago/badge.svg?branch=master)](https://coveralls.io/github/rafalp/Misago?branch=master)
[![Release 0.21](https://img.shields.io/badge/release-0.21-brightgreen.svg)](https://pypi.org/project/Misago/)
[![Works on Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://travis-ci.org/rafalp/Misago)
[![Community Chat](https://img.shields.io/badge/chat-on_discord-7289da.svg)](https://discord.gg/fwvrZgB) 


**Development Status:** 🍌 [Bananas](https://en.wikipedia.org/wiki/Perpetual_beta>) 🍌

Misago aims to be complete, featured and modern forum solution that has no fear to say 'NO' to common and outdated opinions about how forum software should be made and what it should do.

- **Homepage:** http://misago-project.org/
- **Documentation:** https://misago.gitbook.io/docs/
- **Code & BugTracker:** https://github.com/rafalp/Misago/


Screenshots
===========

[![Forum index](https://misago-project.org/media/mporg-home-small.png?01062018)](https://misago-project.org)

[![Thread view](https://misago-project.org/media/mporg-thread-small.png?01062018)](https://misago-project.org)


Production use
==============

As of now Misago implements all features considered "must have" on live internet forum:

* Your users may register accounts, set avatars, change options and edit their profiles. They have option to reset forgotten password.
* Sign in with Facebook, Google, Github, Steam, Blizzard.net or any other over 50 supported OAuth providers.
* Site admins may require users to confirm validity of their e-mail addresses via e-mail sent activation link, or limit user account activation to administrator action. They can use custom Q&A challenge, ReCAPTCHA, Stop Forum Spam or IP's blacklist to combat spam registrations. Pletora of settings are available to control user account behaviour, like username lengths or avatar restrictions.
* Create categories together with unlimited number and depth of subcategories.
* Write messages using either GitHub flavoured markdown, BBCode subset, or both.
* Presence features let site members know when other users are online, offline or banned. Individual users have setting to hide their activity from non-admins.
* Complete moderation toolset allowing admin-approved moderators to edit, move, hide, approve, delete or close user posted content. This also includes option to delete or block user accounts or avatars.
* Ban system allows you to ban existing users as well as forbid certain user names, e-mails or IP addresses from registering accounts.
* Permission system allowing you to control which features are available to users based on their rank, roles or category they are in.
* Post accurate read tracker that lets your users spot threads with new posts as well as let moderators spot unapproved replies and non-moderators spot approved posts.
* Private threads feature allowing users to create threads visible only to them and those they've invited. 
* Python-based profile fields framework letting site owners to define custom fields for users to fill in complete with powerful customization options for custom requirements, display or validation logic.
* Rich polls  system, allowing polls with public and private voters, single and multiple choices as well as ones that allow vote change or limit voting tp limited period of time.
* Post attachments complete thumbnailing and gif's animation removal.
* Mark post in question thread as best answer, bringing basic Q&A functionality.
* Posts edits log allowing you to see how user messages used to look in past as well as revert function protecting you from malignant users emptying their posts contents.
* Moderation queue for users and categories allowing you to moderate content before it becomes visible to other members of the community.
* Custom theme developed over bootstrap.
* Features and settings for achieving GDPR compliance.

Even more features will follow in future releases:

* Achievements and awards system.
* Content reporting for users to report offensive content.
* Forum-wide JS routing further reducing navigation times.
* IP search for moderators to find [sock puppets](https://en.wikipedia.org/wiki/Sockpuppet_(Internet)) or bot nets.
* Notifications for users to notice content and events of concern faster.
* OAuth2 server for those looking to use Misago as auth provider for other apps.
* Warning system for easy tracking users history of infractions and offenses.
* WYSIWYM content editor for even easier post formatting.
* Ranking system for forum search results based on post links, likes, author and thread importance.
* Post reactions in place of likes.

...and more!

If you are looking into using Misago to run live forum, you are absolutely invited to, but please keep in mind that Misago is relatively immature software that may contain serious bugs or issues as well as quirks and lackings thay may take time to resolve, despite best efforts. 


Development
===========

Preferred way to run Misago development instances on your machine is with [Docker](https://www.docker.com/community-edition#/download), which makes it easy to spin up arbitrary number of instances running different code with separate databases and dependencies besides each other.

To start, clone the repository and run `./dev init` command in your terminal. This will build necessary docker containers, install python dependencies and initialize the database. After command does its magic, you will be able to start development server using the `docker-compose up` command.

After development server starts, visit the `http://127.0.0.1:8000/` in your browser to see your Misago installation.

Admin Control Panel is available under the `http://127.0.0.1:8000/admincp/` address. To log in to it use `Admin` username and `password` password.

The `./dev` utility implements other features besides the `init`. Run it without any arguments to get the list of available actions.


Running Misago in development without `dev`
-------------------------------------------

You may skip `./dev init` and setup dev instance manually, running those commands:

1. `docker-compose build` - builds docker containers
2. `docker-compose run --rm misago python manage.py migrate` - runs migrations
3. `docker-compose run --rm misago python manage.py createsuperuser` - creates test user
4. `docker-compose up` - starts dev server


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


Copyright and license
=====================

**Misago** - Copyright © 2018 `Rafał Pitoń <http://github.com/ralfp>`_
This program comes with ABSOLUTELY NO WARRANTY.

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.rst