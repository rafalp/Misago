{% load misago_json %}
window.MisagoData = {{ preloaded_ember_data|as_json }};
