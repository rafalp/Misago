from ...html.element import html_element
from ..upgradepost import upgrade_post_code_blocks


def test_upgrade_post_code_blocks_upgrades_post_code(post):
    post.parsed = html_element(
        "misago-code", "<pre><code>add(1, 2)</code></pre>", {"syntax": "python"}
    )
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert "span" in post.parsed
    assert post.metadata == {}


def test_upgrade_post_code_blocks_skips_upgrade_if_metadata_flag_is_false(post):
    post.parsed = html_element(
        "misago-code", "<pre><code>add(1, 2)</code></pre>", {"syntax": "python"}
    )
    post.metadata["highlight_code"] = False
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed == (
        '<misago-code syntax="python">'
        "<pre><code>add(1, 2)</code></pre>"
        "</misago-code>"
    )
    assert post.metadata == {}


def test_upgrade_post_code_blocks_skips_upgrade_if_metadata_flag_is_not_set(post):
    post.parsed = html_element(
        "misago-code", "<pre><code>add(1, 2)</code></pre>", {"syntax": "python"}
    )
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed == (
        '<misago-code syntax="python">'
        "<pre><code>add(1, 2)</code></pre>"
        "</misago-code>"
    )
    assert post.metadata == {}
