from importlib import import_module

import pytest

from ...attachments.models import Attachment


# migration_module = import_module(
#     "misago.threads.migrations.0018_update_attachments_markup"
# )
# migration = getattr(migration_module, "update_post_attachments_markup")


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_skips_post_without_attachments(post):
    assert not migration(Attachment, post)


@pytest.mark.xfail(reason="broken by misago.posts migration")
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_skips_img_bbcode(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: [img]https://example.com/image.png[/img]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_short_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_short_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_img_bbcode(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_short_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_short_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_img_bbcode(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_media_path_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_media_path_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_media_path_short_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_media_path_short_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_media_path_img_bbcode(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_media_path_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_media_path_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_media_path_short_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_media_path_short_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_media_path_img_bbcode(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_absolute_media_path_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_absolute_media_path_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_absolute_media_path_short_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_absolute_media_path_short_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_absolute_media_path_img_bbcode(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_absolute_media_path_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_absolute_media_path_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_absolute_media_path_short_image(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_absolute_media_path_short_image_with_title(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_absolute_media_path_img_bbcode(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_image_autolink(post, image_attachment):
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_image_thumb_autolink(
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_media_path_autolink(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_media_path_autolink(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_absolute_media_path_autolink(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_replaces_attachment_thumb_absolute_media_path_autolink(
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
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
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


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_skips_url_bbcode(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: [url]https://example.com/image.png[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_skips_url_bbcode_with_text(post):
    post.original = (
        "Hello world!"
        "\n\n"
        "This is link: [url=https://example.com/image.png]Link[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert not migration(Attachment, post)


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_link_with_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [![attachment](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)](https://example.com/image.png)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}> <https://example.com/image.png>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_link_with_short_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [!(/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)](https://example.com/image.png)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}> <https://example.com/image.png>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_link_with_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [some attachment](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: some attachment <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_link_with_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [![attachment](/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_link_with_short_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [!(/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_url_bbcode_with_attachment(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [url]/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_url_bbcode_with_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [url=https://example.com/image.png]![attachment](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <https://example.com/image.png> <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_url_bbcode_with_short_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [url=https://example.com/image.png]!(/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <https://example.com/image.png> <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_url_bbcode_with_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [url=/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1]some attachment[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: some attachment <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_url_bbcode_with_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [url=/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1]![attachment](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_url_bbcode_with_short_attachment_label(
    post, image_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"This is link: [url=/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1]!(/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)[/url]"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"This is link: <attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_link_followed_by_other_attachment_link(
    post, image_attachment, image_thumbnail_attachment
):
    post.original = (
        "Hello world!"
        "\n\n"
        f"[![Zrzut ekranu 2025-01-5 o 13.30.00.png](/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        f"[![Zrzut ekranu 2025-01-5 o 13.32.06.png](/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_thumbnail_attachment.id}/?shva=1)](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_thumbnail_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"<attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )


@pytest.mark.xfail(reason="broken by misago.posts migration")
def test_update_post_attachments_markup_updates_attachment_link_with_attachment_having_space_in_name(
    post, image_attachment
):
    image_attachment.name = "Zrzut ekranu 2025-01-5 o 13.30.00.png"
    image_attachment.save()

    post.original = (
        "Hello world!"
        "\n\n"
        f"[![Zrzut ekranu 2025-01-5 o 13.30.00.png](/a/thumb/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)](/a/sx3otAV3pIuLwIeUJmRLe4oOCUeH62K2kwbupiwqm8H4KMzN5WqjqkvwHUToxlQp/{image_attachment.id}/?shva=1)"
        "\n\n"
        "I hope you've liked it!"
    )
    post.save()

    assert migration(Attachment, post)

    post.refresh_from_db()
    assert post.original == (
        "Hello world!"
        "\n\n"
        f"<attachment={image_attachment.name}:{image_attachment.id}>"
        "\n\n"
        "I hope you've liked it!"
    )
