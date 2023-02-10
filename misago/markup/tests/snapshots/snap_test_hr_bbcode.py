# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_hr_bbcode_is_replaced_if_its_alone_in_paragraph 1"
] = """<p>Lorem ipsum dolor met.</p>
<hr />
<p>Sit amet elit.</p>"""
