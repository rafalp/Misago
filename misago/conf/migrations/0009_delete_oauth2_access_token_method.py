from django.db import migrations


def delete_oauth2_token_method_setting(apps, _):
    Setting = apps.get_model("misago_conf", "Setting")
    Setting.objects.filter(setting="oauth2_token_method").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("misago_conf", "0008_delete_sso_settings"),
    ]

    operations = [migrations.RunPython(delete_oauth2_token_method_setting)]
