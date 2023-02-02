# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_multi_line_code_markdown 1"
] = """<pre><code>&lt;script&gt;
alert(&quot;!&quot;)
&lt;/script&gt;
</code></pre>"""

snapshots[
    "test_multi_line_code_markdown_with_language 1"
] = """<pre><code class="language-javascript">&lt;script&gt;
alert(&quot;!&quot;)
&lt;/script&gt;
</code></pre>"""

snapshots[
    "test_single_line_code_markdown 1"
] = "<p><code>&lt;script&gt;alert(&quot;!&quot;)&lt;/script&gt;</code></p>"
