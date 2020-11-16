# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_bold_bbcode 1"] = "<p>Lorem <b>ipsum</b>!</p>"

snapshots["test_italics_bbcode 1"] = "<p>Lorem <i>ipsum</i>!</p>"

snapshots["test_underline_bbcode 1"] = "<p>Lorem <u>ipsum</u>!</p>"

snapshots[
    "test_inline_bbcode_can_be_mixed_with_markdown 1"
] = "<p>Lorem <b><strong>ipsum</strong></b>!</p>"

snapshots[
    "test_image_bbcode 1"
] = '<p>Lorem <img alt="placekitten.com/g/1200/500" src="https://placekitten.com/g/1200/500"/> ipsum</p>'

snapshots[
    "test_image_bbcode_is_case_insensitive 1"
] = '<p>Lorem <img alt="placekitten.com/g/1200/500" src="https://placekitten.com/g/1200/500"/> ipsum</p>'

snapshots[
    "test_url_bbcode 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="nofollow noopener">placekitten.com/g/1200/500</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="nofollow noopener">dolor</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_long_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="nofollow noopener">dolor met</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_quotes_and_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="nofollow noopener">dolor</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_quotes_and_long_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="nofollow noopener">dolor met</a> ipsum</p>'
