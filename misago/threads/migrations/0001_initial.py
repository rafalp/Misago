import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.search import SearchVectorField
from django.db import migrations, models

import misago.threads.models.attachment


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("misago_categories", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("poster_name", models.CharField(max_length=255)),
                ("poster_ip", models.GenericIPAddressField()),
                ("original", models.TextField()),
                ("parsed", models.TextField()),
                ("checksum", models.CharField(max_length=64, default="-")),
                ("attachments_cache", JSONField(null=True, blank=True)),
                ("posted_on", models.DateTimeField()),
                ("updated_on", models.DateTimeField()),
                ("edits", models.PositiveIntegerField(default=0)),
                (
                    "last_editor_name",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "last_editor_slug",
                    models.SlugField(max_length=255, null=True, blank=True),
                ),
                (
                    "hidden_by",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "hidden_by_name",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "hidden_by_slug",
                    models.SlugField(max_length=255, null=True, blank=True),
                ),
                ("hidden_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("has_reports", models.BooleanField(default=False)),
                ("has_open_reports", models.BooleanField(default=False)),
                ("is_unapproved", models.BooleanField(default=False, db_index=True)),
                ("is_hidden", models.BooleanField(default=False)),
                ("is_protected", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.Category",
                    ),
                ),
                (
                    "last_editor",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "mentions",
                    models.ManyToManyField(
                        related_name="mention_set", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "poster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.SET_NULL,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                ("is_event", models.BooleanField(default=False, db_index=True)),
                ("event_type", models.CharField(max_length=255, null=True, blank=True)),
                ("event_context", JSONField(null=True, blank=True)),
                ("likes", models.PositiveIntegerField(default=0)),
                ("last_likes", JSONField(blank=True, null=True)),
                ("search_document", models.TextField(blank=True, null=True)),
                ("search_vector", SearchVectorField()),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Thread",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.CharField(max_length=255)),
                ("replies", models.PositiveIntegerField(default=0, db_index=True)),
                ("has_events", models.BooleanField(default=False)),
                ("has_poll", models.BooleanField(default=False)),
                ("has_reported_posts", models.BooleanField(default=False)),
                ("has_open_reports", models.BooleanField(default=False)),
                ("has_unapproved_posts", models.BooleanField(default=False)),
                ("has_hidden_posts", models.BooleanField(default=False)),
                ("started_on", models.DateTimeField(db_index=True)),
                ("starter_name", models.CharField(max_length=255)),
                ("starter_slug", models.CharField(max_length=255)),
                ("last_post_is_event", models.BooleanField(default=False)),
                ("last_post_on", models.DateTimeField(db_index=True)),
                (
                    "last_poster_name",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                (
                    "last_poster_slug",
                    models.CharField(max_length=255, null=True, blank=True),
                ),
                ("weight", models.PositiveIntegerField(default=0)),
                ("is_unapproved", models.BooleanField(default=False, db_index=True)),
                ("is_hidden", models.BooleanField(default=False)),
                ("is_closed", models.BooleanField(default=False)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ThreadParticipant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_threads.Thread",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("is_owner", models.BooleanField(default=False)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="thread",
            name="participants",
            field=models.ManyToManyField(
                related_name="privatethread_set",
                through="misago_threads.ThreadParticipant",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="post",
            name="thread",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="misago_threads.Thread"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="thread",
            name="first_post",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="misago_threads.Post",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="thread",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="misago_categories.Category",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="thread",
            name="last_post",
            field=models.ForeignKey(
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to="misago_threads.Post",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="thread",
            name="last_poster",
            field=models.ForeignKey(
                related_name="last_poster_set",
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="thread",
            name="starter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name="thread",
            index_together=set(
                [
                    ("category", "id"),
                    ("category", "last_post_on"),
                    ("category", "replies"),
                ]
            ),
        ),
        migrations.AlterIndexTogether(
            name="post",
            index_together=set(
                [("thread", "id"), ("is_event", "is_hidden"), ("poster", "posted_on")]
            ),
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "last_read_on",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("send_email", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.Category",
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_threads.Thread",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name="subscription", index_together=set([("send_email", "last_read_on")])
        ),
        migrations.CreateModel(
            name="PostEdit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("edited_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("editor_name", models.CharField(max_length=255)),
                ("editor_slug", models.CharField(max_length=255)),
                ("editor_ip", models.GenericIPAddressField()),
                ("edited_from", models.TextField()),
                ("edited_to", models.TextField()),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.Category",
                    ),
                ),
                (
                    "editor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="edits_record",
                        to="misago_threads.Post",
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_threads.Thread",
                    ),
                ),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("secret", models.CharField(max_length=64)),
                (
                    "uploaded_on",
                    models.DateTimeField(
                        default=django.utils.timezone.now, db_index=True
                    ),
                ),
                ("uploader_name", models.CharField(max_length=255)),
                ("uploader_slug", models.CharField(max_length=255, db_index=True)),
                ("uploader_ip", models.GenericIPAddressField()),
                ("filename", models.CharField(max_length=255, db_index=True)),
                ("size", models.PositiveIntegerField(default=0, db_index=True)),
                (
                    "thumbnail",
                    models.ImageField(
                        max_length=255,
                        blank=True,
                        null=True,
                        upload_to=misago.threads.models.attachment.upload_to,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        max_length=255,
                        blank=True,
                        null=True,
                        upload_to=misago.threads.models.attachment.upload_to,
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        max_length=255,
                        blank=True,
                        null=True,
                        upload_to=misago.threads.models.attachment.upload_to,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="misago_threads.Post",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AttachmentType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("extensions", models.CharField(max_length=255)),
                ("mimetypes", models.CharField(blank=True, max_length=255, null=True)),
                ("size_limit", models.PositiveIntegerField(default=1024)),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "Allow uploads and downloads"),
                            (1, "Allow downloads only"),
                            (2, "Disallow both uploading and downloading"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "limit_downloads_to",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_attachmenttype_limit_downloads_to_+",
                        to="misago_acl.Role",
                    ),
                ),
                (
                    "limit_uploads_to",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_attachmenttype_limit_uploads_to_+",
                        to="misago_acl.Role",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="attachment",
            name="filetype",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="misago_threads.AttachmentType",
            ),
        ),
        migrations.AddField(
            model_name="attachment",
            name="uploader",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Poll",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("poster_name", models.CharField(max_length=255)),
                ("poster_slug", models.CharField(max_length=255)),
                ("poster_ip", models.GenericIPAddressField()),
                ("posted_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("length", models.PositiveIntegerField(default=0)),
                ("question", models.CharField(max_length=255)),
                ("choices", django.contrib.postgres.fields.jsonb.JSONField()),
                ("allowed_choices", models.PositiveIntegerField(default=1)),
                ("allow_revotes", models.BooleanField(default=False)),
                ("votes", models.PositiveIntegerField(default=0)),
                ("is_public", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.Category",
                    ),
                ),
                (
                    "poster",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "thread",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_threads.Thread",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PollVote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("voter_name", models.CharField(max_length=255)),
                ("voter_slug", models.CharField(max_length=255)),
                ("voter_ip", models.GenericIPAddressField()),
                ("voted_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("choice_hash", models.CharField(db_index=True, max_length=12)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.Category",
                    ),
                ),
                (
                    "poll",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_threads.Poll",
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_threads.Thread",
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterIndexTogether(
            name="pollvote", index_together=set([("poll", "voter_name")])
        ),
        migrations.CreateModel(
            name="PostLike",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("liker_name", models.CharField(max_length=255, db_index=True)),
                ("liker_slug", models.CharField(max_length=255)),
                ("liker_ip", models.GenericIPAddressField()),
                ("liked_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="misago_categories.Category",
                    ),
                ),
            ],
            options={"ordering": ["-id"]},
        ),
        migrations.AddField(
            model_name="postlike",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="misago_threads.Post"
            ),
        ),
        migrations.AddField(
            model_name="postlike",
            name="thread",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="misago_threads.Thread"
            ),
        ),
        migrations.AddField(
            model_name="postlike",
            name="liker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="liked_by",
            field=models.ManyToManyField(
                related_name="liked_post_set",
                through="misago_threads.PostLike",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
