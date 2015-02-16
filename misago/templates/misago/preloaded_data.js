{% load misago_json %}{% if DEBUG %}// CSRF Token: {{ csrf_token }}{% endif %}
window.MisagoData = {{ preloaded_ember_data|as_json }};
