{% load misago_json %}
window.MisagoData = {
  MISAGO_JS_DEBUG: {{ MISAGO_JS_DEBUG|yesno:"true,false" }},
  misagoSettings: {{ misago_settings.get_public_settings|as_json }},
  staticUrl: "{{ STATIC_URL }}",
  mediaUrl: "{{ MEDIA_URL }}"
}
