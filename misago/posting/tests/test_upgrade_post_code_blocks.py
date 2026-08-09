from html import escape

from ...html.element import html_element
from ..upgradepost import upgrade_post_code_blocks


def test_upgrade_post_code_blocks_upgrades_post_code(post):
    post.content_parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.content_parsed.startswith('<misago-code syntax="python">')
    assert post.content_parsed.endswith("</misago-code>")
    assert "span" in post.content_parsed
    assert post.metadata == {}


def test_upgrade_post_code_blocks_upgrades_escaped_code(post):
    post.content_parsed = html_element(
        "misago-code", escape('echo("<code>")'), {"syntax": "php"}
    )
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.content_parsed.startswith('<misago-code syntax="php">')
    assert post.content_parsed.endswith("</misago-code>")
    assert "echo(&quot;&lt;code&gt;&quot;)" in post.content_parsed
    assert '"<code>"' not in post.content_parsed
    assert post.metadata == {}


def test_upgrade_post_code_blocks_upgrades_multiple_code_blocks(post):
    post.content_parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.content_parsed += "<p>Hello</p>"
    post.content_parsed += html_element("misago-code", "add(1, 2)", {"syntax": "php"})
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert "<p>Hello</p>" in post.content_parsed
    assert "span" in post.content_parsed
    assert post.metadata == {}


def test_upgrade_post_code_blocks_handles_unsupported_syntax(post):
    post.content_parsed = html_element(
        "misago-code", "add(1, 2)", {"syntax": "invalid"}
    )
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert (
        post.content_parsed == '<misago-code syntax="invalid">add(1, 2)</misago-code>'
    )
    assert post.metadata == {}


def test_upgrade_post_code_blocks_handles_unspecified_syntax(post):
    post.content_parsed = html_element("misago-code", "add(1, 2)")
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.content_parsed == "<misago-code>add(1, 2)</misago-code>"
    assert post.metadata == {}


def test_upgrade_post_code_blocks_skips_upgrade_if_metadata_flag_is_false(post):
    post.content_parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.metadata["highlight_code"] = False
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.content_parsed == (
        '<misago-code syntax="python">add(1, 2)</misago-code>'
    )
    assert post.metadata == {}


def test_upgrade_post_code_blocks_skips_upgrade_if_metadata_flag_is_not_set(post):
    post.content_parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.content_parsed == (
        '<misago-code syntax="python">add(1, 2)</misago-code>'
    )
    assert post.metadata == {}
