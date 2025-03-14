from ...html.element import html_element
from ..upgradepost import upgrade_post_content


def test_upgrade_post_content_upgrades_post_code(post):
    post.parsed = html_element(
        "misago-code", "<pre><code>add(1, 2)</code></pre>", {"syntax": "python"}
    )
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_content(post)

    post.refresh_from_db()
    assert "span" in post.parsed
    assert post.metadata == {}
