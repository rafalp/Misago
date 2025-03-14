from html import escape

from ...html.element import html_element
from ..upgradepost import upgrade_post_code_blocks


def test_upgrade_post_code_blocks_upgrades_post_code(post):
    post.parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed.startswith('<misago-code syntax="python">')
    assert post.parsed.endswith("</misago-code>")
    assert "span" in post.parsed
    assert post.metadata == {}


def test_upgrade_post_code_blocks_upgrades_escaped_code(post):
    post.parsed = html_element(
        "misago-code", escape('echo("<code>")'), {"syntax": "php"}
    )
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed.startswith('<misago-code syntax="php">')
    assert post.parsed.endswith("</misago-code>")
    assert "echo(&quot;&lt;code&gt;&quot;)" in post.parsed
    assert '"<code>"' not in post.parsed
    assert post.metadata == {}


def test_upgrade_post_code_blocks_upgrades_multiple_code_blocks(post):
    post.parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.parsed += "<p>Hello</p>"
    post.parsed += html_element("misago-code", "add(1, 2)", {"syntax": "php"})
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert "<p>Hello</p>" in post.parsed
    assert "span" in post.parsed
    assert post.metadata == {}


def test_upgrade_post_code_blocks_handles_unsupported_syntax(post):
    post.parsed = html_element("misago-code", "add(1, 2)", {"syntax": "invalid"})
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed == '<misago-code syntax="invalid">add(1, 2)</misago-code>'
    assert post.metadata == {}


def test_upgrade_post_code_blocks_handles_unspecified_syntax(post):
    post.parsed = html_element("misago-code", "add(1, 2)")
    post.metadata["highlight_code"] = True
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed == "<misago-code>add(1, 2)</misago-code>"
    assert post.metadata == {}


def test_upgrade_post_code_blocks_skips_upgrade_if_metadata_flag_is_false(post):
    post.parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.metadata["highlight_code"] = False
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed == ('<misago-code syntax="python">' "add(1, 2)" "</misago-code>")
    assert post.metadata == {}


def test_upgrade_post_code_blocks_skips_upgrade_if_metadata_flag_is_not_set(post):
    post.parsed = html_element("misago-code", "add(1, 2)", {"syntax": "python"})
    post.save()

    upgrade_post_code_blocks(post)

    post.refresh_from_db()
    assert post.parsed == ('<misago-code syntax="python">' "add(1, 2)" "</misago-code>")
    assert post.metadata == {}
