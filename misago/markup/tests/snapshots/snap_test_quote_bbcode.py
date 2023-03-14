# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_multi_line_quote 1"
] = """<aside class="quote-block">
<div class="quote-heading" data-noquote="1"></div>
<blockquote class="quote-body" data-block="quote">
<p>Sit amet elit.</p>
<p>Another line.</p>
</blockquote>
</aside>"""

snapshots[
    "test_quote_can_contain_bbcode_or_markdown 1"
] = """<aside class="quote-block">
<div class="quote-heading" data-noquote="1"></div>
<blockquote class="quote-body" data-block="quote">
<p>Sit <strong>amet</strong> <u>elit</u>.</p>
</blockquote>
</aside>"""

snapshots[
    "test_quotes_can_be_nested 1"
] = """<aside class="quote-block">
<div class="quote-heading" data-noquote="1"></div>
<blockquote class="quote-body" data-block="quote">
<p>Sit amet elit.</p>
<aside class="quote-block">
<div class="quote-heading" data-noquote="1"></div>
<blockquote class="quote-body" data-block="quote">
<p>Nested quote</p>
</blockquote>
</aside>
</blockquote>
</aside>"""

snapshots[
    "test_quotes_can_contain_hr_markdown 1"
] = """<aside class="quote-block">
<div class="quote-heading" data-noquote="1"></div>
<blockquote class="quote-body" data-block="quote">
<p>Sit amet elit.</p>
<hr />
<p>Another line.</p>
</blockquote>
</aside>"""

snapshots[
    "test_single_line_authored_quote 1"
] = """<aside class="quote-block">
<div class="quote-heading" data-noquote="1">@Bob</div>
<blockquote class="quote-body" data-author="@Bob" data-block="quote">
<p>Sit amet elit.</p>
</blockquote>
</aside>"""

snapshots[
    "test_single_line_authored_quote_without_quotations 1"
] = """<aside class="quote-block">
<div class="quote-heading" data-noquote="1">@Bob</div>
<blockquote class="quote-body" data-author="@Bob" data-block="quote">
<p>Sit amet elit.</p>
</blockquote>
</aside>"""

snapshots[
    "test_single_line_quote 1"
] = """<aside class="quote-block">
<div class="quote-heading" data-noquote="1"></div>
<blockquote class="quote-body" data-block="quote">
<p>Sit amet elit.</p>
</blockquote>
</aside>"""
