from django.test import TestCase

from misago.api import context_processors


class MockRequest(object):
    pass


class FrontendContextTests(TestCase):
    def test_frontend_context(self):
        """frontend_context is available in templates"""
        mock_request = MockRequest()
        mock_request.include_frontend_context = True
        mock_request.frontend_context = {'someValue': 'Something'}

        self.assertEqual(
            context_processors.frontend_context(mock_request), {
                'frontend_context': {
                    'someValue': 'Something',
                },
            }
        )

        mock_request.include_frontend_context = False
        self.assertEqual(context_processors.frontend_context(mock_request), {})
