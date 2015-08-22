{% load misago_json %}{% if DEBUG %}// CSRF Token: {{ csrf_token }}{% endif %}
misago.preloaded_data = {{ preloaded_ember_data|as_json }};
