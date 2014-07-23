=======================
Template Tags Reference
=======================

Misago defines plenty of custom tags and filters for use by template authors.


misago_avatars
=============

``avatar`` filter
-----------------

Accepts user model instance or integer representing user's PK, returns link to avatar server that can be used as ``src`` attribute value for ``img``.

Takes one optional argument, image size.


``blankavatar`` tag
-------------------

Returns link to avatar blank avatar that can be used as ``src`` attribute value for ``img``. Should be used when no user pk is avaialable to render avatar, eg. displaying items belonging to deleted users.

Takes one optional argument, image size.


misago_capture
==============

``capture as`` tag
------------------

Captures part of template to variable that may then be displayed many more times.

There is also trimmed flavour ``capture trimmed as`` that trims captured template part before assinging it to variable.


misago_editor
=============

``editor_body`` tag
-------------------

Renders Misago Markup editor body in template. Requires one argument: variable containing editor instance.


``editor_js`` tag
-----------------

Renders Misago Markup editor's javascript in template. Requires one argument: variable containing editor instance.


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
