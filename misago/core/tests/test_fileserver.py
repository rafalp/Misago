import os

from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.test import TestCase

from misago.core import fileserver


class FileServerTests(TestCase):
    def test_send_file(self):
        """send file produces valid response"""
        with self.settings(MISAGO_SENDFILE_HEADER='X-Test'):
            response = fileserver.make_file_response(__file__, 'text/python')
            self.assertTrue(isinstance(response, HttpResponse))
            self.assertEqual(response['X-Test'], __file__)

        with self.settings(MISAGO_SENDFILE_HEADER=''):
            response = fileserver.make_file_response(__file__, 'text/python')
            self.assertTrue(isinstance(response, StreamingHttpResponse))

    def test_rewrite_file_path(self):
        """file paths are rewritten"""
        with self.settings(MISAGO_SENDFILE_LOCATIONS_PATH='mymisagopath'):
            test_path = '%s/somefile.png' % settings.MISAGO_AVATAR_CACHE
            rewritten_path = fileserver.rewrite_file_path(test_path)
            self.assertTrue(rewritten_path.startswith('/mymisagopath/'))

            with self.assertRaises(ValueError):
                fileserver.rewrite_file_path('some/non_rewrriten/path.zip')

    def test_send_header(self):
        """call to header response function returns HttpResponse"""
        with self.settings(MISAGO_SENDFILE_HEADER='X-Test'):
            response = fileserver.make_header_response(
                __file__, 'text/python', 9)
            self.assertTrue(isinstance(response, HttpResponse))
            self.assertEqual(response['X-Test'], __file__)

    def test_send_stream(self):
        """call to streaming response function returns StreamingHttpResponse"""
        response = fileserver.make_stream_response(__file__, 'text/python', 9)
        self.assertTrue(isinstance(response, StreamingHttpResponse))
