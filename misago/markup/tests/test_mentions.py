from misago.markup.mentions import add_mentions
from misago.users.testutils import AuthenticatedUserTestCase


class MockRequest(object):
    def __init__(self, user):
        self.user = user


class MentionsTests(AuthenticatedUserTestCase):
    def test_single_mention(self):
        """markup extension parses single mention"""
        TEST_CASES = [
            ('<p>Hello, @{}!</p>', '<p>Hello, <a href="{}">@{}</a>!</p>'),
            ('<h1>Hello, @{}!</h1>', '<h1>Hello, <a href="{}">@{}</a>!</h1>'),
            ('<div>Hello, @{}!</div>', '<div>Hello, <a href="{}">@{}</a>!</div>'),
            (
                '<h1>Hello, <strong>@{}!</strong></h1>',
                '<h1>Hello, <strong><a href="{}">@{}</a>!</strong></h1>'
            ),
            (
                '<h1>Hello, <strong>@{}</strong>!</h1>',
                '<h1>Hello, <strong><a href="{}">@{}</a></strong>!</h1>'
            ),
        ]

        for before, after in TEST_CASES:
            result = {'parsed_text': before.format(self.user.username), 'mentions': []}

            add_mentions(MockRequest(self.user), result)

            outcome = after.format(self.user.get_absolute_url(), self.user.username)
            self.assertEqual(result['parsed_text'], outcome)
            self.assertEqual(result['mentions'], [self.user])

    def test_invalid_mentions(self):
        """markup extension leaves invalid mentions alone"""
        TEST_CASES = [
            '<p>Hello, Bob!</p>',
            '<p>Hello, @Bob!</p>',
            '<p>Hello, <a href="/">@{}</a>!</p>'.format(self.user.username),
            '<p>Hello, <a href="/"><b>@{}</b></a>!</p>'.format(self.user.username),
        ]

        for markup in TEST_CASES:
            result = {'parsed_text': markup, 'mentions': []}

            add_mentions(MockRequest(self.user), result)

            self.assertEqual(result['parsed_text'], markup)
            self.assertFalse(result['mentions'])

    def test_multiple_mentions(self):
        """markup extension handles multiple mentions"""
        before = '<p>Hello @{0} and @{0}, how is it going?</p>'.format(self.user.username)

        after = '<p>Hello <a href="{0}">@{1}</a> and <a href="{0}">@{1}</a>, how is it going?</p>'.format(
            self.user.get_absolute_url(), self.user.username
        )

        result = {'parsed_text': before, 'mentions': []}

        add_mentions(MockRequest(self.user), result)
        self.assertEqual(result['parsed_text'], after)
        self.assertEqual(result['mentions'], [self.user])

    def test_repeated_mention(self):
        """markup extension handles mentions across document"""
        before = '<p>Hello @{0}</p><p>@{0}, how is it going?</p>'.format(self.user.username)

        after = '<p>Hello <a href="{0}">@{1}</a></p><p><a href="{0}">@{1}</a>, how is it going?</p>'.format(
            self.user.get_absolute_url(), self.user.username
        )

        result = {'parsed_text': before, 'mentions': []}

        add_mentions(MockRequest(self.user), result)
        self.assertEqual(result['parsed_text'], after)
        self.assertEqual(result['mentions'], [self.user])
