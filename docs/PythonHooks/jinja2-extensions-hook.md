# `jinja2_extensions_hook`

A `list` of [Jinja extensions](https://jinja.palletsprojects.com/en/2.10.x/extensions/#jinja-extensions) that should be used by template engine:

```python
from misago.template.hooks import register_routes_hook

register_routes_hook.appendd(...)
```