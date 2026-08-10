from ...html.element import html_element
from ..processcontent import process_post_content


def test_process_post_content_highlights_code(post):
    post.content_parsed = html_element(
        "misago-code", "<pre><code>add(1, 2)</code></pre>", {"syntax": "python"}
    )
    post.metadata["highlight_code"] = True
    post.save()

    process_post_content(post)

    post.refresh_from_db()
    assert "span" in post.content_parsed
    assert post.metadata == {}
