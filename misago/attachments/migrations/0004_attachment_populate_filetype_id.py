# Generated by Django 4.2.10 on 2025-01-06 13:04

from django.db import migrations

from ..filetypes import filetypes


def populate_attachments_filetypes_names(apps, _):
    Attachment = apps.get_model("misago_attachments", "Attachment")

    for attachment in Attachment.objects.order_by("id").iterator(chunk_size=50):
        filetype = filetypes.match_filetype(attachment.name)
        if filetype:
            attachment.filetype_id = filetype.id
            attachment.save(update_fields=["filetype_id"])


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("misago_attachments", "0003_attachment_populate_category_thread"),
    ]

    operations = [
        migrations.RunPython(
            populate_attachments_filetypes_names,
            migrations.RunPython.noop,
        ),
    ]
