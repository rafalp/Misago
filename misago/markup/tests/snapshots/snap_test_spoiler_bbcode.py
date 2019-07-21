# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_single_line_spoiler 1"
] = """<aside class="spoiler-block">
<div class="spoiler-heading"></div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Daenerys and Jon live happily ever after!</p>
</blockquote>
</aside>"""

snapshots[
    "test_single_line_spoiler_can_have_custom_title 1"
] = """<aside class="spoiler-block">
<div class="spoiler-heading">GoT Ending</div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Daenerys and Jon live happily ever after!</p>
</blockquote>
</aside>"""

snapshots[
    "test_single_line_spoiler_can_have_custom_title_without_quotations 1"
] = """<aside class="spoiler-block">
<div class="spoiler-heading">GoT Ending</div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Daenerys and Jon live happily ever after!</p>
</blockquote>
</aside>"""

snapshots[
    "test_spoiler_can_contain_bbcode_or_markdown 1"
] = """<aside class="spoiler-block">
<div class="spoiler-heading"></div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Sit <strong>amet</strong> <u>elit</u>.</p>
</blockquote>
</aside>"""

snapshots[
    "test_multi_line_spoiler 1"
] = """<aside class="spoiler-block">
<div class="spoiler-heading"></div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Sit amet elit.</p>
<p>Another line.</p>
</blockquote>
</aside>"""

snapshots[
    "test_spoilers_can_be_nested 1"
] = """<aside class="spoiler-block">
<div class="spoiler-heading"></div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Sit amet elit.</p>
<aside class="spoiler-block">
<div class="spoiler-heading"></div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Nested spoiler</p>
</blockquote>
</aside>
</blockquote>
</aside>"""

snapshots[
    "test_spoilers_can_contain_hr_markdown 1"
] = """<aside class="spoiler-block">
<div class="spoiler-heading"></div>
<button class="spoiler-reveal" type="button"></button><blockquote class="spoiler-body">
<p>Sit amet elit.</p>
<hr/>
<p>Another line.</p>
</blockquote>
</aside>"""
