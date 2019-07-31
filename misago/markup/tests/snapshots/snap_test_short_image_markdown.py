# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_short_image_markdown 1"
] = '<p><img alt="somewhere.com/image.jpg" src="http://somewhere.com/image.jpg"/></p>'
