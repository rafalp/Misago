# `jinja2_filters_hook`

A `dict` of [Jinja filters](https://jinja.palletsprojects.com/en/2.10.x/api/#custom-filters) that should be used by template engine:

```python
from misago.template.hooks import jinja2_filters_hook

jinja2_filters_hook["exception"] = my_exception
```