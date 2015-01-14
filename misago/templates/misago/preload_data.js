{% load misago_json%}
MisagoPreloadStore.set("misago_settings", {{ misago_settings.get_public_settings|as_json }});
MisagoPreloadStore.set("staticUrl", "{{ STATIC_URL }}");
MisagoPreloadStore.set("mediaUrl", "{{ MEDIA_URL }}");
