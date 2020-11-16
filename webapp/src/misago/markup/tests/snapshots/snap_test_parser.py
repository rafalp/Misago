# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_html_is_escaped 1"] = "<p>Lorem &lt;strong&gt;ipsum!&lt;/strong&gt;</p>"

snapshots[
    "test_parsed_text_is_minified 1"
] = "<p>Lorem <strong>ipsum</strong> dolor met.</p><p>Sit amet elit.</p>"
