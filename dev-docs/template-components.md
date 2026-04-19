# Template components

In Misago, a "template component" is a template file and a Python dict with a `template_name` key that is a string containing the template file's name:

```python
# Minimal template component:
template_component = {
    "template_name": "my_template.html",
}
```

```html
<!-- my_template.html -->
<div>Hello! I am a template to include!</div>
```

If the `dict` defines other keys, they are merged with the parent template's context when rendering the component:

```python
# In "my_template.html", the `user` value will be overridden
template_component = {
    "template_name": "my_template.html",
    "user": other_user,
}
```

```html
<!-- my_template.html -->
<div>Hello {{ user }}! I am a template to include!</div>
```


## Including template components

To include a template component in another template, use the `includecomponent` tag from the `misago_component` module:

```html
{% load misago_component %}

{% includecomponent template_component %}
```

Because `template_component` is a Python dict, you can still use standard Django template logic around `includecomponent`:

```html
{% load misago_component %}

{% if footer_component %}
    <div>
        {% includecomponent template_component %}
    </div>
{% else %}
    <div>fallback!</div>
{% endif %}
```


# Including lists of template components

To include multiple template components in a single place in a template, use the `includecomponents` tag from the `misago_component` module.

```python
extra_messages = [
    {"template_name": "welcome_message.html"},
    {"template_name": "monthly_promo_message.html"},
]
```

```html
{% load misago_component %}

{% if extra_messages %}
    <div class="extra-messages">
        {% includecomponents extra_messages %}
    </div>
{% endif %}
```