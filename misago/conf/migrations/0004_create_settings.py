# Generated by Django 2.2.1 on 2019-05-19 00:16

from django.conf import settings
from django.db import migrations

from ..hydrators import dehydrate_value

default_settings = [
    {"setting": "account_activation", "dry_value": "none", "is_public": True},
    {"setting": "allow_custom_avatars", "python_type": "bool", "dry_value": True},
    {
        "setting": "avatar_upload_limit",
        "python_type": "int",
        "dry_value": 1536,
        "is_public": True,
    },
    {"setting": "attachment_403_image", "python_type": "image"},
    {"setting": "attachment_404_image", "python_type": "image"},
    {"setting": "blank_avatar", "python_type": "image"},
    {"setting": "captcha_type", "dry_value": "no", "is_public": True},
    {"setting": "default_avatar", "dry_value": "gravatar"},
    {"setting": "default_gravatar_fallback", "dry_value": "dynamic"},
    {"setting": "unused_attachments_lifetime", "python_type": "int", "dry_value": 24},
    {"setting": "email_footer"},
    {
        "setting": "forum_address",
        "dry_value": getattr(settings, "MISAGO_ADDRESS", None),
        "is_public": True,
    },
    {"setting": "forum_footnote", "is_public": True},
    {"setting": "forum_name", "dry_value": "Misago", "is_public": True},
    {"setting": "google_tracking_id"},
    {"setting": "google_site_verification"},
    {"setting": "index_header", "is_public": True},
    {"setting": "index_meta_description", "is_public": True},
    {"setting": "index_title", "is_public": True},
    {"setting": "logo", "python_type": "image", "is_public": True},
    {"setting": "logo_small", "python_type": "image", "is_public": True},
    {"setting": "logo_text", "dry_value": "Misago", "is_public": True},
    {"setting": "daily_post_limit", "python_type": "int", "dry_value": 600},
    {"setting": "hourly_post_limit", "python_type": "int", "dry_value": 100},
    {"setting": "post_attachments_limit", "python_type": "int", "dry_value": 16},
    {
        "setting": "post_length_max",
        "python_type": "int",
        "dry_value": 60000,
        "is_public": True,
    },
    {
        "setting": "post_length_min",
        "python_type": "int",
        "dry_value": 5,
        "is_public": True,
    },
    {"setting": "readtracker_cutoff", "python_type": "int", "dry_value": 40},
    {"setting": "threads_per_page", "python_type": "int", "dry_value": 26},
    {"setting": "posts_per_page", "python_type": "int", "dry_value": 18},
    {"setting": "posts_per_page_orphans", "python_type": "int", "dry_value": 6},
    {"setting": "events_per_page", "python_type": "int", "dry_value": 20},
    {"setting": "og_image", "python_type": "image"},
    {
        "setting": "og_image_avatar_on_profile",
        "python_type": "bool",
        "dry_value": False,
    },
    {"setting": "og_image_avatar_on_thread", "python_type": "bool", "dry_value": False},
    {"setting": "qa_answers"},
    {"setting": "qa_help_text"},
    {"setting": "qa_question"},
    {"setting": "recaptcha_secret_key"},
    {"setting": "recaptcha_site_key", "is_public": True},
    {
        "setting": "signature_length_max",
        "python_type": "int",
        "dry_value": 256,
        "is_public": True,
    },
    {"setting": "subscribe_reply", "dry_value": "watch_email"},
    {"setting": "subscribe_start", "dry_value": "watch_email"},
    {
        "setting": "thread_title_length_max",
        "python_type": "int",
        "dry_value": 90,
        "is_public": True,
    },
    {
        "setting": "thread_title_length_min",
        "python_type": "int",
        "dry_value": 5,
        "is_public": True,
    },
    {"setting": "username_length_min", "python_type": "int", "dry_value": 3},
    {"setting": "username_length_max", "python_type": "int", "dry_value": 14},
    {"setting": "stop_forum_spam", "python_type": "bool", "dry_value": False},
    {"setting": "stop_forum_spam_confidence", "python_type": "int", "dry_value": 80},
    {"setting": "users_per_page", "python_type": "int", "dry_value": 12},
    {"setting": "users_per_page_orphans", "python_type": "int", "dry_value": 4},
]

removed_settings = ["forum_branding_display", "forum_branding_text"]


def create_settings(apps, _):
    # This migration builds list of existing settings, and then
    # creates settings not already in the database
    Setting = apps.get_model("misago_conf", "Setting")

    # Update existing settings and add new ones
    existing_settings = list(Setting.objects.values_list("setting", flat=True))
    for setting in default_settings:
        if setting["setting"] in existing_settings:
            continue  # skip already existing setting (migration on existing forum)

        data = setting.copy()
        if "python_type" in data and "dry_value" in data:
            data["dry_value"] = dehydrate_value(data["python_type"], data["dry_value"])

        Setting.objects.create(**setting)

    # Delete deprecated settings
    Setting.objects.filter(setting__in=removed_settings).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("misago_conf", "0003_simplify_models"),
        ("misago_core", "0003_delete_cacheversion"),
        ("misago_threads", "0012_set_dj_partial_indexes"),
        ("misago_users", "0020_set_dj_partial_indexes"),
    ]

    operations = [migrations.RunPython(create_settings)]
