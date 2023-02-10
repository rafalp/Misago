# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_bold_bbcode 1"] = "<p>Lorem <b>ipsum</b>!</p>"

snapshots[
    "test_image_bbcode 1"
] = '<p>Lorem <img alt="placekitten.com/g/1200/500" src="https://placekitten.com/g/1200/500" /> ipsum</p>'

snapshots[
    "test_image_bbcode_is_case_insensitive 1"
] = '<p>Lorem <img alt="placekitten.com/g/1200/500" src="https://placekitten.com/g/1200/500" /> ipsum</p>'

snapshots[
    "test_image_bbcode_is_escaped 1"
] = '<p>Lorem <img alt="&lt;script language=&quot;application/javascript&quot;&gt;" src="http://&lt;script language=&quot;application/javascript&quot;&gt;" /> ipsum</p>'

snapshots["test_inline_bbcode_can_be_mixed 1"] = "<p>Lorem <b><u>ipsum</u></b>!</p>"

snapshots[
    "test_inline_bbcode_can_be_mixed_with_markdown 1"
] = "<p>Lorem <b><strong>ipsum</strong></b>!</p>"

snapshots["test_italics_bbcode 1"] = "<p>Lorem <i>ipsum</i>!</p>"

snapshots[
    "test_simple_inline_bbcode_is_escaped 1"
] = "<p>Lorem <b>ips &lt;script language=&quot;application/javascript&quot;&gt; um</b>!</p>"

snapshots["test_underline_bbcode 1"] = "<p>Lorem <u>ipsum</u>!</p>"

snapshots[
    "test_url_bbcode 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="external nofollow noopener" target="_blank">placekitten.com/g/1200/500</a> ipsum</p>'

snapshots[
    "test_url_bbcode_is_escaped 1"
] = '<p>Lorem <a href="http://&lt;script language=&quot;application/javascript&quot;&gt;" rel="external nofollow noopener" target="_blank">&lt;script language=&quot;application/javascript&quot;&gt;</a> ipsum</p>'

snapshots[
    "test_url_bbcode_link_text_is_escaped 1"
] = '<p>Lorem <a href="http://&lt;script language=&quot;application/javascript&quot;&gt;" rel="external nofollow noopener" target="_blank">&lt;script language=&quot;application/javascript&quot;&gt;</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="external nofollow noopener" target="_blank">dolor</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_long_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="external nofollow noopener" target="_blank">dolor met</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_quotes_and_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="external nofollow noopener" target="_blank">dolor</a> ipsum</p>'

snapshots[
    "test_url_bbcode_with_quotes_and_long_link_text 1"
] = '<p>Lorem <a href="https://placekitten.com/g/1200/500" rel="external nofollow noopener" target="_blank">dolor met</a> ipsum</p>'
