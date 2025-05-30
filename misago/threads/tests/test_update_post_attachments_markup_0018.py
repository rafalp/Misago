from importlib import import_module

from ...attachments.models import Attachment

migration_module = import_module(
    "misago.threads.migrations.0018_update_attachments_markup"
)
migration = getattr(migration_module, "update_post_attachments_markup")


def test_update_post_attachments_markup_skips_post_without_attachments(post):
    assert not migration(Attachment, post)


def test_update_post_attachments_markup_skips_image(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: ![Image](https://example.com/image.png)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


def test_update_post_attachments_markup_skips_short_image(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: !(https://example.com/image.png)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)
