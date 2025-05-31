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


def test_update_post_attachments_markup_skips_image_with_title(post):
    post.original = (
        "Hello world!"
        "\n\n"
        'This is link: ![Image](https://example.com/image.png "Hello world")'
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


def test_update_post_attachments_markup_skips_short_image_with_title(post):
    post.original = (
        "Hello world!"
        "\n\n"
        'This is link: !(https://example.com/image.png "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


def test_update_post_attachments_markup_skips_image_bbcode(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: [img]https://example.com/image.png[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


def test_update_post_attachments_markup_updates_attachment_image(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: ![Image](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_image_with_title(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: ![Image](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1 "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_short_image(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: !(/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_short_image_with_title(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: !(/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1 "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_image_bbcode(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [img]/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_thumb_image(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: ![Image](/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_thumb_image_with_title(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: ![Image](/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1 "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_thumb_short_image(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: !(/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_thumb_short_image_with_title(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: !(/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1 "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_thumb_image_bbcode(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [img]/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>" in post.original
    )


def test_update_post_attachments_markup_updates_attachment_media_path_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: ![Image]({image_thumbnail_attachment.upload.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_media_path_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: ![Image]({image_thumbnail_attachment.upload.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_media_path_short_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: !({image_thumbnail_attachment.upload.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_media_path_short_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: !({image_thumbnail_attachment.upload.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_media_path_image_bbcode(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [img]{image_thumbnail_attachment.upload.url}[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_media_path_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: ![Image]({image_thumbnail_attachment.thumbnail.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_media_path_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: ![Image]({image_thumbnail_attachment.thumbnail.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_media_path_short_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: !({image_thumbnail_attachment.thumbnail.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_media_path_short_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: !({image_thumbnail_attachment.thumbnail.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_media_path_image_bbcode(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [img]{image_thumbnail_attachment.thumbnail.url}[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_absolute_media_path_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: ![Image](http://example.com{image_thumbnail_attachment.upload.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_absolute_media_path_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: ![Image](http://example.com{image_thumbnail_attachment.upload.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_absolute_media_path_short_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: !(http://example.com{image_thumbnail_attachment.upload.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_absolute_media_path_short_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: !(http://example.com{image_thumbnail_attachment.upload.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_absolute_media_path_image_bbcode(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [img]http://example.com{image_thumbnail_attachment.upload.url}[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_absolute_media_path_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: ![Image](https://example.com{image_thumbnail_attachment.thumbnail.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_absolute_media_path_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: ![Image](https://example.com{image_thumbnail_attachment.thumbnail.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_absolute_media_path_short_image(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: !(https://example.com{image_thumbnail_attachment.thumbnail.url})"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_absolute_media_path_short_image_with_title(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f'This is link: !(https://example.com{image_thumbnail_attachment.thumbnail.url} "Hello world")'
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_absolute_media_path_image_bbcode(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [img]https://example.com{image_thumbnail_attachment.thumbnail.url}[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_skips_autolink(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: <https://example.com/image.png>"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


def test_update_post_attachments_markup_updates_image_autolink(post, image_attachment):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: </a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1>"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_image_thumb_autolink(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: </a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1>"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_attachment.name}:{image_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_media_path_autolink(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: <{image_thumbnail_attachment.upload.url}>"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_media_path_autolink(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: <{image_thumbnail_attachment.thumbnail.url}>"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_absolute_media_path_autolink(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: <https://example.com{image_thumbnail_attachment.upload.url}>"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_updates_attachment_thumb_absolute_media_path_autolink(
    post, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: <https://example.com{image_thumbnail_attachment.thumbnail.url}>"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert (
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
    ) in post.original


def test_update_post_attachments_markup_skips_link(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: [Link](https://example.com/image.png)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


def test_update_post_attachments_markup_skips_link_bbcode(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: [url]https://example.com/image.png[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


def test_update_post_attachments_markup_skips_link_bbcode_with_text(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: [url=https://example.com/image.png]Link[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)
