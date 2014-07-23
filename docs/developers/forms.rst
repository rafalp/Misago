=====================
Using Forms in Misago
=====================

.. note::
   Purpose of this document is to introduce you to differences and features of forms module available in misago.core.forms package.

   For proper introduction to forums, see `Django documentation <https://docs.djangoproject.com/en/dev/topics/forms/>`_.


Misago extends standard forms library that comes with Django with extra components. First one is `Crispy Forms <http://django-crispy-forms.readthedocs.org/en/latest/>`_ app that allows to use templates to display forms. Thanks to this feature, it's possible to render correct markup that `Bootstrap <getbootstrap.com/css/#forms>`_ requires with minimal amount of effort.


Misago Forms Module
===================

Second extension lies in :py:mod:`misago.core.forms` module that imports Django forms. This layer introduces tiny convenience change to forms standard clean and validate behaviour that will save you from some "gotchas" associated with input length validation. Unlike other popular frameworks and solutions, Django does not automatically trim input values received from client before validation, which means user can enter few spaces into text fields instead of "readable" value and such input will pass automatical validation and will need additional cleanup and checks in custom ``clean_`` methods. Because there's good chance your app will have plenty of ``CharField`` fields, such boilerplate can quickly add up.

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

Wrapper for :py:class:`django.forms.Form` that uses AutoStripWhitespacesMixin.


ModelForm
---------

:py:class:`misago.core.forms.ModelForm`

Wrapper for :py:class:`django.forms.ModelForm` that uses AutoStripWhitespacesMixin.


YesNoSwitch
-----------

:py:func:`misago.core.forms.YesNoSwitch`

Thin wrapper around Django's ``TypedChoiceField``. This field renders nice yes/no switch as its input.

.. warning::
   ``YesNoSwitch`` coerces to ``int``, not to ``bool``! Remember about this when writing code dealing with forms containing this field!


Template Tags
=============

Misago defines custom templates extension named ``misago_forms``. This extension contains two template tags for rendering form fields:


form_row
--------

This tag takes form field as its first argument and renders field complete with label, help and errors. Accept two extra arguments: label class and field class, allowing you to control size of horizontal forms::


    {% load misago_forms %}

    {% form_row form.somefield %}
    {% form_row form.otherfield 'col-md-3' 'col-md-9' %}


form_input
----------

This tag takes form field as its only argument and renders it's input.
