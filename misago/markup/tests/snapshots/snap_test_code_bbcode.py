# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_code_block_disables_parsing 1"
] = "<pre><code>Dolor [b]met.[/b]</code></pre>"

snapshots[
    "test_code_with_language_parameter 1"
] = '<pre><code class="language-php">echo(&quot;Hello!&quot;);</code></pre>'

snapshots[
    "test_code_with_quoted_language_parameter 1"
] = '<pre><code class="language-php">echo(&quot;Hello!&quot;);</code></pre>'

snapshots[
    "test_multi_line_code 1"
] = """<pre><code>&lt;script&gt;
alert(&quot;!&quot;)
&lt;/script&gt;</code></pre>"""

snapshots[
    "test_single_line_code 1"
] = "<pre><code>echo(&quot;Hello!&quot;);</code></pre>"
