# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_short_image_markdown[base] 1"
] = '<p><img alt="somewhere.com/image.jpg" src="http://somewhere.com/image.jpg" /></p>'

snapshots[
    "test_short_image_markdown[space-multiple-words] 1"
] = "<p>! (space with other words)</p>"

snapshots["test_short_image_markdown[space-one-word] 1"] = "<p>! (space)</p>"

snapshots[
    "test_short_image_markdown[text-before-mark] 1"
] = '<p>Text before exclamation mark<img alt="somewhere.com/image.jpg" src="http://somewhere.com/image.jpg" /></p>'

snapshots[
    "test_short_image_markdown[text-before-with-space] 1"
] = "<p>Text before with space in between! (sometext)</p>"
