=====================
Using Forms in Misago
=====================

.. note::
   Purpose of this document is to introduce you to differences and features of forms module available in misago.core.forms package.

   For proper introduction to forums, see `Django documentation <https://docs.djangoproject.com/en/dev/topics/forms/>`_.


Misago wraps standard forms library that comes with Django with two extra layers layers of abstraction. First one is `Django-floppyforms <http://django-floppyforms.readthedocs.org/en/latest/>`_ app that allows to use templates to display forms.
 Thanks to this feature, it's possible to render correct markup that `Bootstrap <getbootstrap.com/css/#forms>`_ requires with minimal amount of efford.


Misago Forms Module
===================

Second layer lies in :py:mod:`misago.core.forms` module that wraps floppyforms. This layer introduces tiny convenience change to forms standard clean and validate behaviour that will save you from some "gotchas" associated with input length validation. Unlike other popular frameworks and solutions, Django does not automatically trim input values received from client before validation, which means user can enter few spaces into text fields instead of "readable" value and such input will pass automatical validation and will need additional cleanup and checks in custom ``clean_`` methods. Because there's good chance your app will have plenty of ``CharField`` fields, such boilerplate can quickly add up.

In :py:mod:`misago.core.forms` you will find three classes:


AutoStripWhitespacesMixin
-------------------------

:py:class:`misago.core.forms.AutoStripWhitespacesMixin`

Small mixin that strips whitespaces from all ``CharField``'s input on form, before its passed further for validation.

If you wish to exclude one or more fields from this behaviour, you may add their names to "autostrip_exclude" attribute::


    class MyLargeForm(Form):
        autostrip_exclude = ['i_wont_be_stripped']
        i_will_be_stripped = forms.CharField()
        i_wont_be_stripped = forms.CharField()


Form
----

:py:class:`misago.core.forms.Form`

Wrapper for :py:class:`floppyforms.Form` that uses AutoStripWhitespacesMixin.


ModelForm
---------

:py:class:`misago.core.forms.ModelForm`

Wrapper for :py:class:`floppyforms.ModelForm` that uses AutoStripWhitespacesMixin.


Picking Layer
-------------

Each of namespaces mentioned here, be it :py:mod:`django.forms`, :py:mod:`floppyforms` or :py:mod:`misago.core.forms` imports previous namespace, which means after you import :py:mod:`floppyforms`, you don't have to import :py:mod:`django.forms` too.

When writing custom forms, please avoid using :py:mod:`django.forms`, instead using either :py:mod:`floppyforms` or :py:mod:`floppyforms`.
