============================
Coding Style and Conventions
============================

When writing Python code for Misago, please familiarize yourself with and follow those documents:

1. `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_
2. `Django Coding Style and Conventions <https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>`_

Those documents should give you solid knowledge of coding style and conventions that are followed by Python and Django programmers when writing code.

In addition to those guidelines, Misago defines set of additional convetions and good practices that will help you write better and easier code:


Models
======

Fields Order
------------

When declaring model's database fields, start with taxonomical foreign keys followed by fields that make this model identifiable to humans. Order of remaining fileds is completely up to you.

Thread model is great example of this convention. Thread is part of taxonomy (Forum), so first field defined is foreign key to Forum model. This is followed by two fields that humans will use to recognise this model: "title" that will be displayed in UI and "slug" that will be included in links to this thread. After those Thread model defines additional fields.

When declaring model database fields, make sure they are grouped together based on their purpose. Most common example is storage of user name and slug in addition to foreign key to User model. In such case, make sure both "poster" field as well as "poster_name", "poster_slug" and "poster_ip" fields are grouped together.


Avoid Unmeaningful Names
------------------------

Whenever possible avoid naming fields representing relation to "User" model "user". Preffer more descriptive names like "poster", "last_editor", or "giver".

For same reason avoid using "date" or "ip" as field names. Use more descriptive "posted_on" or "poster_ip" instead.


True/False Fields
-----------------

For extra clarity prefix fields representing true/false states of model with "is". "is_deleted" is better than "deleted".


URLConfs
========

Link names should correspond to views and patterns whenever possible. This means that link pointing to "user_warnings" view should be named "user_warnings" and should match "user/rafalp-1/warnings/". This makes associating patterns, links and views easy for those trying to understand your code.

Avoid temptation to prefix links with app names. Good link name should point at correct app without that. If there's name collision, you should rethink your views because there's chance you are either repeating yourself or planned your app structure incorrectly.

Links pointing at classes instead of functions should use lowercase letters and undersores. This means that link pointing at "ForumThreads" should be named "forum_threads".

If link parameters correspond to model fields, name them after those. If your link contains model's pk and slug, name those parameters pk and slug. If link contains parameter that represents foreign key or pk of other model, don't suffix it with "_id" or "_pk". For example link to edit reply in thread can define parameters "pk" and "slug" that are used to fetch thread from database and additional "reply" parameter that will be used to identify reply in thread's reply_set.


Views and Forms
===============

Depending on number of views in your app, you may have single "views.py" file (AKA python module), or "views" directory (AKA python package). While both approaches are perfectly valid, you should preffer first one and only switch to latter when your views module becomes too big. Same practice applies for "forms.py". Split it only when file becomes to big to be easily navigate.

In addition to views and forms definitions, those files can also contain helper functions and attributes. Your views may perform same logic that you may want to move to single decorator or mixin in order to DRY your code while your forms may define factories or dynamic default values. However file contents should always follow "what it says on the tin" rule. If your views module defines forms or has nothing else but mixins or decorators that are imported by other modules, it shouldn't be named "views".

.. note::
   This rule is not specific just for views and forms files or even for python language ans is widely considered as good practice in majority of programming languages out there.


View Arguments
--------------

As convention, declare view arguments in same order parameters are declared in view's links patterns.

Templates
=========

.. note::
   There is no silver bullet approach to how you should name or organize templates in your apps. Instead in this chapter will explain convention used by Misago.

