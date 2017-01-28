Template Tags Reference
=======================

Misago defines plenty of custom tags and filters for use by template authors.


## `misago_batch`

There are situations when you want to slice list of items in template into sublists, e.g. when displaying grid of items in HTML it makes more sense to split iteration into two steps: iteration over rows and items in each row.

`misago_batch` provides two simple and lazy filters that enable you to do this:


### `{{ itemslist|batch:4 }}`

Takes one argument, integer individual batch's length, then turns big list into list of lists.


```
{% load misago_batch %}

{% for row in user_profiles|batch:4 %}
    <div class="row">
        {% for profile in row %}
            <div class="col-md-3">
                {% include "card.html" %}
            </div>
        {% endfor %}
    </div>
{% endfor %}
```


### `{{ itemslist|batchnonefilled:4 }}`

Works same as `batch` filter, but with one difference:

If last batch length is shorter than requested, it fills it with `None` to make it requested length.

```
{% load misago_batch %}

{% for row in user_profiles|batchnonefilled:4 %}
    <div class="row">
        {% for profile in row %}
            <div class="col-md-3">
                {% if profile %}
                    {% include "card.html" %}
                {% else %}
                    &nbsp;
                {% endif %}
            </div>
        {% endfor %}
    </div>
{% endfor %}
```


## `misago_capture`

### `{% capture as NAME %}{% endcapture %}`

Captures part of template to variable that may then be displayed many more times.

There is also trimmed flavour `{% capture trimmed as NAME %}{% endcapture %}` that trims captured template part before assinging it to variable.


## `misago_dates`

### `{{ item.posted_on|compact_date }}`

Filter that formats date according to format defines in `MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH` setting if date is in current year, or `MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH_YEAR` if not. Defaults to "7 may" for same year dates and "may '13" for past years dates.


## `misago_forms`

### `{% form_row form.field labelclass fieldclass%}`

Takes form field as its first argument and renders field complete with label, help and errors. Accept two extra arguments: label class and field class, allowing you to control size of horizontal forms:

```
{% load misago_forms %}

{% form_row form.somefield %}
{% form_row form.otherfield 'col-md-3' 'col-md-9' %}
```


### `{% form_input %}`

Takes form field as its only argument and renders it's input.


## `misago_json`

### `{{ frontend_context|as_json }}`

Turns value into json string. Perfoms additional escaping on `<` signs so `</script>` are not interpreted as HTML resulting in XSS.


## misago_shorthands

### `{{ 'this is outputed'|iftrue:test }}`

Shorthand for simple if clauses: `{{ "fade in"|iftrue:thread.is_closed }}` will render `fade in` in template if `thread.is_closed` evaluates to `True`.


### `{{ 'this is outputed'|iffalse:test }}`

Opposite to `iftrue`. Outputs value if test evaluates to `False`.