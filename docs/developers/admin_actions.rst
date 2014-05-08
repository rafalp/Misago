=========================
Writing New Admin Actions
=========================


Misago Admin vs. Django Admin
=============================

Misago brings its own admin site just like Django `does <https://docs.djangoproject.com/en/1.6/#the-admin>`_. This means you have to make a decision which one your app will use for administration.

If you intend to be sole user of your app, Django admin will propably be faster to get going. However if you plan for your app to be available to wider audience, its good for your admin interface to be part of Misago admin site. This will require you to write more code than intended, but will give your users more consistent experience and, in case for some languages, save them of quirkyness that comes with django admin automatic messages.


Writing Admin Views
===================


Registering in Misago Admin
===========================

Misago Admin Site is just an hierarchy of links defined in apps and registered within ``misago.admin.site`` object.


Registering urls under ``misago:admin`` namespace
-------------------------------------------------

Your admin views will live under ``misago:admin`` namespace, which means they should be defined in special manner. Similiarly to Django, Misago uses small discovery routine which finds patterns belonging to its admin namespace.


Depending on structure of your app and your tastes, you can define your admin patterns in one of three ways:

* as **adminurlpatterns** variable in **yourapp.urls** module
* as **urlpatterns** variable in **yourapp.urls.admin** module
* as **urlpatterns** variable in **yourapp.adminurls** module

Each of those is checked, but only first one to be found is used.
