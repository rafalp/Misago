=======================
Template Tags Reference
=======================

Misago defines plenty of custom tags and filters for use by template authors.


misago_batch
============

There are situations when you want to slice list of items in template into sublists, e.g. when displaying grid of items in HTML it makes more sense to split iteration into two steps: iteration over rows and items in each row.

``misago_batch`` provides two simple and lazy filters that enable you to do this:


``batch`` filter
----------------

Takes one argument, integer individual batch length, then turns big list into list of lists.


``batchnonefilled`` filter
--------------------------

Works same as ``batch`` filter, but with one difference:

If last batch length is shorter than requested, it fills it with ``None`` to make it requested length.


misago_capture
==============

``capture as`` tag
------------------

Captures part of template to variable that may then be displayed many more times.

There is also trimmed flavour ``capture trimmed as`` that trims captured template part before assinging it to variable.


misago_dates
============

``compact_date`` filter
-----------------------

Filter that formats date according to format defines in ``MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH`` setting if date is in current year, or ``MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH_YEAR`` if not. Defaults to "7 may" for same year dates and "may '13" for past years dates.


misago_editor
=============

``editor_body`` tag
-------------------

Renders Misago Markup editor body in template. Requires one argument: variable containing editor instance.


misago_forms
============

``form_row`` tag
----------------

Takes form field as its first argument and renders field complete with label, help and errors. Accept two extra arguments: label class and field class, allowing you to control size of horizontal forms::


    {% load misago_forms %}

    {% form_row form.somefield %}
    {% form_row form.otherfield 'col-md-3' 'col-md-9' %}


``form_input`` tag
------------------

Takes form field as its only argument and renders it's input.


misago_json
============

``as_json`` filter
------------------

Turns value into json string.


misago_shorthands
=================

``iftrue`` filter
-----------------

Shorthand for simple if clauses: ``{{ "fade in"|iftrue:thread.is_closed }}`` will render ``"fade in"`` in template if ``thread.is_closed`` is true.


``iffalse`` filter
-----------------

Opposite filter for ``iftrue``.
