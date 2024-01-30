# Generated by Django 4.2.8 on 2024-01-27 12:54

from django.db import migrations

from misago.conf.hydrators import dehydrate_value

settings = [
    {
        "setting": "oauth2_enable_pkce",
        "python_type": "bool",
        "wet_value": False,
        "is_public": False,
    },
    {
        "setting": "oauth2_pkce_code_challenge_method",
        "dry_value": "S256",
        "is_public": False,
    },
]


def create_settings(apps, _):
    Setting = apps.get_model("misago_conf", "Setting")
    for setting in settings:
        data = setting.copy()
        if "python_type" in data and "wet_value" in data:
            data["dry_value"] = dehydrate_value(
                data["python_type"], data.pop("wet_value")
            )

        Setting.objects.create(**data)


def remove_settings(apps, _):
    Setting = apps.get_model("misago_conf", "Setting")
    for setting in settings:
        Setting.objects.filter(setting=setting["setting"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("misago_conf", "0011_add_notifications_settings"),
    ]

    operations = [migrations.RunPython(create_settings, remove_settings)]
