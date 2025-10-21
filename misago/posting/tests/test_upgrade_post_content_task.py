import pytest

from ...html.element import html_element
from ...threads.models import Post
from ..tasks import upgrade_post_content


def test_upgrade_post_content_task_raises_post_does_not_exist_for_invalid_post_id(db):
    with pytest.raises(Post.DoesNotExist):
        upgrade_post_content(1, "checksum")


def test_upgrade_post_content_task_does_nothing_if_post_has_invalid_checksum(post):
    upgrade_post_content(post.id, "invalid-checksum")


def test_upgrade_post_content_task_logs_exceptions(mocker, post):
    mock_logger = mocker.patch("misago.posting.tasks.logger")
    mock_upgrade_post_content = mocker.patch(
        "misago.posting.upgradepost.upgrade_post_content",
        side_effect=ValueError(),
    )

    upgrade_post_content(post.id, post.sha256_checksum)

    mock_logger.exception.assert_called_once()
    mock_upgrade_post_content.assert_called_once_with(post)


def test_upgrade_post_content_task_upgrades_post_code(post):
    post.parsed = html_element(
        "misago-code", "<pre><code>add(1, 2)</code></pre>", {"syntax": "python"}
    )
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_content(post.id, post.sha256_checksum)

    post.refresh_from_db()
    assert "span" in post.parsed
    assert post.metadata == {}
