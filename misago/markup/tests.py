from django.test import TestCase

from misago.markup.parser import parse
from misago.markup import checksums


class ParserTests(TestCase):
    def test_inline_text(self):
        """inline elements are correctly parsed"""
        test_text = """
Lorem **ipsum** dolor met.

Lorem [b]ipsum[/b] [i]dolor[/i] [u]met[/u].

Lorem [b]**ipsum**[/b] [i]dolor[/i] [u]met[/u].

Lorem [b]**ipsum[/b]** [i]dolor[/i] [u]met[/u].

Lorem [b]__ipsum[/b]__ [i]dolor[/i] [u]met[/u].

Lorem [b][i]ipsum[/i][/b].

Lorem [b][i]ipsum[/b][/i].

Lorem [b]ipsum[/B].
""".strip()

        expected_result = """
<p>Lorem <strong>ipsum</strong> dolor met.</p>
<p>Lorem <b>ipsum</b> <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b><strong>ipsum</strong></b> <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b>**ipsum</b>** <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b>__ipsum</b>__ <i>dolor</i> <u>met</u>.</p>
<p>Lorem <b><i>ipsum</i></b>.</p>
<p>Lorem <b>[i]ipsum</b>[/i].</p>
<p>Lorem <b>ipsum</b>.</p>
""".strip()

        result = parse(test_text)
        self.assertEqual(expected_result, result['parsed_text'])

    def test_blocks(self):
        """block elements are correctly parsed"""
        test_text = """
Lorem ipsum.
[hR]
Dolor met.
""".strip()

        expected_result = """
<p>Lorem ipsum.</p>
<hr/>
<p>Dolor met.</p>
""".strip()

        result = parse(test_text)
        self.assertEqual(expected_result, result['parsed_text'])


class ChecksupTests(TestCase):
    def test_checksums(self):
        fake_message = "<p>Woow, thats awesome!</p>"
        post_pk = 231

        checksum = checksums.make_checksum(fake_message, [post_pk])

        self.assertTrue(
            checksums.is_checksum_valid(fake_message, checksum, [post_pk]))
        self.assertFalse(
            checksums.is_checksum_valid(fake_message, checksum, [3]))



