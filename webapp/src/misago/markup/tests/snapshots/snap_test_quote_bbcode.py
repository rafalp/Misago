# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_single_line_quote 1"
] = """<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Sit amet elit.</p>
</blockquote>
</aside>"""

snapshots[
    "test_single_line_authored_quote 1"
] = """<aside class="quote-block">
<div class="quote-heading">@Bob</div>
<blockquote class="quote-body">
<p>Sit amet elit.</p>
</blockquote>
</aside>"""

snapshots[
    "test_single_line_authored_quote_without_quotations 1"
] = """<aside class="quote-block">
<div class="quote-heading">@Bob</div>
<blockquote class="quote-body">
<p>Sit amet elit.</p>
</blockquote>
</aside>"""

snapshots[
    "test_quote_can_contain_bbcode_or_markdown 1"
] = """<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Sit <strong>amet</strong> <u>elit</u>.</p>
</blockquote>
</aside>"""

snapshots[
    "test_multi_line_quote 1"
] = """<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Sit amet elit.</p>
<p>Another line.</p>
</blockquote>
</aside>"""

snapshots[
    "test_quotes_can_be_nested 1"
] = """<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Sit amet elit.</p>
<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Nested quote</p>
</blockquote>
</aside>
</blockquote>
</aside>"""

snapshots[
    "test_quotes_can_contain_hr_markdown 1"
] = """<aside class="quote-block">
<div class="quote-heading"></div>
<blockquote class="quote-body">
<p>Sit amet elit.</p>
<hr/>
<p>Another line.</p>
</blockquote>
</aside>"""
