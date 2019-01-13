# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_simple_url_to_file_is_replaced_with_valid_url 1"
] = '.page-header { background-image: url("/media/themes/themedir/media/test.357c2ee3.png"); }'

snapshots[
    "test_relative_url_to_file_is_replaced_with_valid_url 1"
] = '.page-header { background-image: url("/media/themes/themedir/media/test.357c2ee3.png"); }'

snapshots[
    "test_url_to_file_from_create_react_app_is_replaced_with_valid_url 1"
] = '.page-header { background-image: url("/media/themes/themedir/media/test.357c2ee3.png"); }'

snapshots[
    "test_quoted_url_to_file_is_replaced_with_valid_url 1"
] = '.page-header { background-image: url("/media/themes/themedir/media/test.357c2ee3.png"); }'

snapshots[
    "test_single_quoted_url_to_file_is_replaced_with_valid_url 1"
] = '.page-header { background-image: url("/media/themes/themedir/media/test.357c2ee3.png"); }'

snapshots[
    "test_css_file_with_multiple_different_urls_is_correctly_replaced 1"
] = """.page-header { background-image: url(http://cdn.example.com/bg.png); }
.container { background-image: url("/media/themes/themedir/media/test.357c2ee3.png"); }
.alert { background-image: url("g"); }"""
