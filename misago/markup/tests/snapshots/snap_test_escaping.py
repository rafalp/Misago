# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_code_in_quote_bbcode_is_escaped 1"
] = """<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>&lt;script&gt;alert("!")&lt;/script&gt;</p>
</blockquote>
</aside>"""

snapshots[
    "test_code_in_quote_markdown_is_escaped 1"
] = """<blockquote>
<p>&lt;script&gt;alert("!")&lt;/script&gt;</p>
</blockquote>"""

snapshots[
    "test_inline_code_is_escaped 1"
] = '<p><code>&lt;script&gt;alert("!")&lt;/script&gt;</code></p>'

snapshots["test_text_is_escaped 1"] = '<p>&lt;script&gt;alert("!")&lt;/script&gt;</p>'
