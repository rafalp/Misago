============================
Coding Style and Conventions
============================

When writing Python code for Misago, please familiarize yourself with and follow those documents:

1. `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_
2. `Django Coding Style and Conventions <https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>`_

Those documents should give you solid knowledge of coding style and conventions that are followed by Python and Django programmers when writing code.

In addition to those guidelines, Misago defines set of additional convetions and good practices that will help you write better and easier code:


Writing Models
==============

Fields Order
------------

When declaring model's database fields, start with taxonomical foreign keys followed by fields that make this model identifiable to humans. Order of remaining fileds is completely up to you.

Thread model is great example of this convention. Thread is part of taxonomy (Forum), so first field defined is foreign key to Forum model. This is followed by two fields that fields humans will use to recognise this model: "title" that will be displayed in UI and "slug" that will be included in links to this thread.

When declaring model database fields, make sure they are grouped together based on their purpose. Most common example is storage of user name and slug in addition to foreign key to User model. In such case, make sure both "poster" field as well as "poster_name", "poster_slug" and "poster_ip" fields are grouped together.


Avoid Unmeaningful Names
------------------------

Whenever possible avoid naming fields representing relation to "User" model "user". Preffer more descriptive names like "poster", "last_editor", or "giver".

For same reason avoid using "date" or "ip" as field names. Use more descriptive "posted_on" or "poster_ip" instead.


True/False Fields
-----------------

For extra clarity prefix fields representing true/false states of model with "is". "is_deleted" is better than "deleted".


Writing Views
=============



URLConfs
========
