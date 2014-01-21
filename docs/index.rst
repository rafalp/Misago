====================
Welcome to Misago documentation!
====================

Misago is featured internet forum solution developed in accordance with practices and trends currently used in web software development.

Like in any full stack solution, Misago provides different levels of interaction that allow for fullfilling different use cases. People who come to your site to talk with each other and exchange their opinions and knowledge will most likely asociate Misago with what they see in their browsers, while developers that are developing site around Misago will focus on its code, API's and implementations details.

The goal of Misago documentation is to provide refence and explanation of features available on each of the stack's layers.

.. warning::
   Documentation is currently in early Work in Progress state. New documents are added as features they cover are implemented, with exception of "Users" part of documentation which will be worked on once Misago reaches beta testing stage.


System Administrators
=====================

System Administrators are users with direct access to server resources and services. This section covers Misago setup and update processes as well as live site maintenance.

.. toctree::
   :maxdepth: 1

   setup_maintenance


Users
=====

This part of documentation is aimed at users who interact with Misago by the graphical UI available through internet browser. It's divided in three parts, with first one aimed for guests and signed in members posting on your forums, second one at moderators tasked by maintaining friendly atmosphere and finally third one for those who want to improve their knowledge and understanding of administration tools available in Admin Control Panel.

1. User Manual
2. Moderator Manual
3. Administrator Manual


Developers
==========

Misago is being developed with customizability and extensibility on mind and offers many features for those looking into modifying its look and feel, extending its featurebase or changing behaviour of core features.

And if this isn't enough for you, Misago itself stands on shoulders of `Django <https://www.djangoproject.com/>`_, powerful and battle-tested web framework with great documentation and rich ecosystem of additional modules (named "apps"). This means Misago is not "just forum solution". Its also complete framework you may use to build your entire site around, writing your own Django apps or `installing and adapting one of thousands ready apps freely available in the internet <http://djangopackages.com/>`_.

No matter what you are trying to accomplish, Misago has you covered.


Customizing Appearance
----------------------

Misago appearance is product of many different technologies acting together to produce final result that you and your users see in their browsers.

On server side powerful, performant and extensible template engine named `Jinja2 <http://jinja.pocoo.org/>`_ turns template files into final html that is displayed in browser while asset pipeline compiles, merges and optimizes less, css and javascript files making your browser load faster and relieving you from burden of compressing and optimizing them yourself.

On browser side Misago comes with it's own UI framework that uses `Bootstrap <http://getbootstrap.com>`_, `jQuery <http://jquery.org>`_ as well Glyphicons and `Font Awesome <http://fontawesome.io>`_ as it's foundations that allows you to provide smooth, pleasant and modern experience to your site's users.


Writing Extensions
------------------

Misago extensions are called "apps". Each "app" can be either single feature like extra user profile tab or entire set of many features working together to add whole new part to your site like user blogs or galleries or file downloads.

To offer such level of extensibility many parts of Misago (and Django too!) were designed as simple and lightweight frameworks to which that you can add (or remove) features.

Following references cover everything you want to know about writing your own apps for Misago. From them you will learn what coding style, conventions and best practices you should follow when writing your code. Next you will be shown how to add your own pages and models to Misago and what features are available for you in doing so. Finally all available frameworks will be presented with explanation what they are used for and how you can add your features to them.

.. toctree::
   :maxdepth: 1

   coding_style