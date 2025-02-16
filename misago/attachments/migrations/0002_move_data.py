# Generated by Django 4.2.10 on 2024-09-07 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("misago_attachments", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            """
            INSERT INTO misago_attachments_attachment (
                id,
                post_id,
                uploader_id,
                uploader_name,
                uploader_slug,
                uploaded_at,
                name,
                upload,
                size,
                thumbnail,
                thumbnail_size,
                is_deleted,
                plugin_data
            )
            SELECT
                id,
                post_id,
                uploader_id,
                uploader_name,
                uploader_slug,
                uploaded_on,
                filename,
                image,
                size,
                thumbnail,
                0,
                'false',
                plugin_data::jsonb
            FROM misago_threads_attachment;
            """,
            migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            """
            UPDATE misago_attachments_attachment a
            SET upload = b.file
            FROM misago_threads_attachment b
            WHERE (
                a.id = b.id
                AND (a.upload = '')
            );
            """,
            migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            """
            SELECT SETVAL(
                'misago_attachments_attachment_id_seq',
                (SELECT last_value FROM misago_threads_attachment_id_seq)
            );
            """,
            migrations.RunSQL.noop,
        ),
    ]
