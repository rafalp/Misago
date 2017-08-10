Context processors
==================

Context Processors are simple python functions that receive HttpRequest object and extend template context with additional values. In addition to [default context processors defined by Django](https://docs.djangoproject.com/en/dev/ref/templates/api/#subclassing-context-requestcontext), Misago defines its own context processors:


## `misago.core.context_processors.frontend_context`

Exposes `frontend_context` to templates, allowing you to JSON serialize and pass it to JavaScript frontend:

```
{% load misago_json %}

<script type="text/javascript">
  const context = {{ frontend_context|as_json }};
  misago.init(context);
</script>
```


## `misago.core.context_processors.site_address`

This function adds `SITE_ADDRESS` value to template context that you can use to build absolue links in your templates:

```
# Will become "http://mysite.com/users/"
{{ SITE_ADDRESS }}{% url 'misago:users' %}
```

This is most useful for links in e-mail templates.
