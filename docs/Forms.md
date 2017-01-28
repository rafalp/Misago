Forms
=====

Purpose of this document is to introduce you to differences and features of forms module available in `misago.core.forms` package.

For proper introduction to forms, see [Django documentation](https://docs.djangoproject.com/en/{{ book.django_version }}/topics/forms/).

Because Misago relies on JSON API endpoints to change application state by users, bulk of forms are be written as React.js components making AJAX requests to different `/api/` edges, either bypassing the forms altogether, or using them purely for data validation and cleaning.

Misago's admin uses [Crispy Forms](http://django-crispy-forms.readthedocs.org/en/latest/) app that allows to easily display forms using `Bootstrap 3` markup.

Finally, Misago defines few custom field types:


### `misago.core.forms.YesNoSwitch`

Thin wrapper around Django's `TypedChoiceField`. In admin this field renders nice yes/no switch as its input.


##### Warning!

`YesNoSwitch` coerces its value to `int` (eg. `0` or `1`)! Remember about this when writing code dealing with forms containing this field!


## Template tags

Misago defines custom templates extension named `misago_forms`. This extension contains two template tags for rendering form fields:


### `form_row`

This tag takes form field as its first argument and renders field complete with label, help and errors. Accepts two extra arguments: label class and field class, allowing you to control size of horizontal forms:

```
{% load misago_forms %}

{% form_row form.somefield %}
{% form_row form.otherfield 'col-md-3' 'col-md-9' %}
```


### `form_input`

This tag takes form field as its only argument and renders it's input.