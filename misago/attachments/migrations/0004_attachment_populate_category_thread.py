# Generated by Django 4.2.10 on 2024-09-10 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("misago_attachments", "0003_attachment_category_thread_is_deleted"),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE
                misago_attachments_attachment a
            SET
                category_id = p.category_id,
                thread_id = p.thread_id
            FROM
                misago_threads_post p
            WHERE
                a.post_id = p.id;
            """,
            migrations.RunSQL.noop,
        ),
    ]
