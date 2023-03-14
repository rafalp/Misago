# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_multi_line_spoiler 1"
] = """<aside class="spoiler-block">
<blockquote class="spoiler-body" data-block="spoiler">
<p>Sit amet elit.</p>
<p>Another line.</p>
</blockquote>
<div class="spoiler-overlay" data-noquote="1"><button class="spoiler-reveal" type="button"></button></div>
</aside>"""

snapshots[
    "test_single_line_spoiler 1"
] = """<aside class="spoiler-block">
<blockquote class="spoiler-body" data-block="spoiler">
<p>Daenerys and Jon live happily ever after!</p>
</blockquote>
<div class="spoiler-overlay" data-noquote="1"><button class="spoiler-reveal" type="button"></button></div>
</aside>"""

snapshots[
    "test_spoiler_can_contain_bbcode_or_markdown 1"
] = """<aside class="spoiler-block">
<blockquote class="spoiler-body" data-block="spoiler">
<p>Sit <strong>amet</strong> <u>elit</u>.</p>
</blockquote>
<div class="spoiler-overlay" data-noquote="1"><button class="spoiler-reveal" type="button"></button></div>
</aside>"""

snapshots[
    "test_spoilers_can_be_nested 1"
] = """<aside class="spoiler-block">
<blockquote class="spoiler-body" data-block="spoiler">
<p>Sit amet elit.</p>
<aside class="spoiler-block">
<blockquote class="spoiler-body" data-block="spoiler">
<p>Nested spoiler</p>
</blockquote>
<div class="spoiler-overlay" data-noquote="1"><button class="spoiler-reveal" type="button"></button></div>
</aside>
</blockquote>
<div class="spoiler-overlay" data-noquote="1"><button class="spoiler-reveal" type="button"></button></div>
</aside>"""

snapshots[
    "test_spoilers_can_contain_hr_markdown 1"
] = """<aside class="spoiler-block">
<blockquote class="spoiler-body" data-block="spoiler">
<p>Sit amet elit.</p>
<hr />
<p>Another line.</p>
</blockquote>
<div class="spoiler-overlay" data-noquote="1"><button class="spoiler-reveal" type="button"></button></div>
</aside>"""
