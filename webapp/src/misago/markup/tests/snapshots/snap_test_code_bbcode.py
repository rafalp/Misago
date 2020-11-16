# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_single_line_code 1"] = '<pre><code>echo("Hello!");</code></pre>'

snapshots[
    "test_multi_line_code 1"
] = """<pre><code>echo("Hello!");

echo("World!");</code></pre>"""

snapshots[
    "test_code_with_language_parameter 1"
] = '<pre><code class="php">echo("Hello!");</code></pre>'

snapshots[
    "test_code_with_quoted_language_parameter 1"
] = '<pre><code class="php">echo("Hello!");</code></pre>'

snapshots[
    "test_code_block_disables_parsing 1"
] = "<pre><code>Dolor [b]met.[/b]</code></pre>"
