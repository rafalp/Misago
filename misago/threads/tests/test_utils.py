from unittest import expectedFailure

from django.test import TestCase

from ..utils import get_thread_id_from_url


class MockRequest:
    def __init__(self, scheme, host, wsgialias=""):
        self.scheme = scheme
        self.host = host

        self.path_info = "/api/threads/123/merge/"
        self.path = "%s%s" % (wsgialias.rstrip("/"), self.path_info)

    def get_host(self):
        return self.host

    def is_secure(self):
        return self.scheme == "https"


class GetThreadIdFromUrlTests(TestCase):
    @expectedFailure
    def test_get_thread_id_from_valid_urls(self):
        """get_thread_id_from_url extracts thread pk from valid urls"""
        TEST_CASES = [
            {
                # perfect match
                "request": MockRequest("https", "testforum.com", "/discuss/"),
                "url": "https://testforum.com/discuss/t/test-thread/123/",
                "pk": 123,
            },
            {
                # we don't validate scheme in case site recently moved to https
                # but user still has old url's saved somewhere
                "request": MockRequest("http", "testforum.com", "/discuss/"),
                "url": "http://testforum.com/discuss/t/test-thread/432/post/12321/",
                "pk": 432,
            },
            {
                # extract thread id from other thread urls
                "request": MockRequest("https", "testforum.com", "/discuss/"),
                "url": "http://testforum.com/discuss/t/test-thread/432/post/12321/",
                "pk": 432,
            },
            {
                # extract thread id from thread page url
                "request": MockRequest("http", "testforum.com", "/discuss/"),
                "url": "http://testforum.com/discuss/t/test-thread/432/123/",
                "pk": 432,
            },
            {
                # extract thread id from thread last post url with relative schema
                "request": MockRequest("http", "testforum.com", "/discuss/"),
                "url": "//testforum.com/discuss/t/test-thread/18/last/",
                "pk": 18,
            },
            {
                # extract thread id from url that lacks scheme
                "request": MockRequest("http", "testforum.com", ""),
                "url": "testforum.com/t/test-thread/12/last/",
                "pk": 12,
            },
            {
                # extract thread id from schemaless thread last post url
                "request": MockRequest("http", "testforum.com", "/discuss/"),
                "url": "testforum.com/discuss/t/test-thread/18/last/",
                "pk": 18,
            },
            {
                # extract thread id from url that lacks scheme and hostname
                "request": MockRequest("http", "testforum.com", ""),
                "url": "/t/test-thread/13/",
                "pk": 13,
            },
            {
                # extract thread id from url that has port name
                "request": MockRequest("http", "127.0.0.1:8000", ""),
                "url": "https://127.0.0.1:8000/t/test-thread/13/",
                "pk": 13,
            },
            {
                # extract thread id from url that isn't trimmed
                "request": MockRequest("http", "127.0.0.1:8000", ""),
                "url": "   /t/test-thread/13/   ",
                "pk": 13,
            },
        ]

        for case in TEST_CASES:
            pk = get_thread_id_from_url(case["request"], case["url"])
            self.assertEqual(
                pk,
                case["pk"],
                "get_thread_id_from_url for %(url)s should return %(pk)s" % case,
            )

    def test_get_thread_id_from_invalid_urls(self):
        TEST_CASES = [
            {
                # lacking wsgi alias
                "request": MockRequest("https", "testforum.com"),
                "url": "http://testforum.com/discuss/t/test-thread-123/",
            },
            {
                # invalid wsgi alias
                "request": MockRequest("https", "testforum.com", "/discuss/"),
                "url": "http://testforum.com/forum/t/test-thread-123/",
            },
            {
                # invalid hostname
                "request": MockRequest("http", "misago-project.org", "/discuss/"),
                "url": "https://testforum.com/discuss/t/test-thread-432/post/12321/",
            },
            {
                # old thread url
                "request": MockRequest("http", "testforum.com"),
                "url": "https://testforum.com/thread/test-123/",
            },
            {
                # dashed thread url
                "request": MockRequest("http", "testforum.com"),
                "url": "https://testforum.com/t/test-thread-123/",
            },
            {
                # non-thread url
                "request": MockRequest("http", "testforum.com"),
                "url": "https://testforum.com/user/user-123/",
            },
            {
                # rubbish url
                "request": MockRequest("http", "testforum.com"),
                "url": "asdsadsasadsaSA&das8as*S(A*sa",
            },
            {
                # blank url
                "request": MockRequest("http", "testforum.com"),
                "url": "/",
            },
            {
                # empty url
                "request": MockRequest("http", "testforum.com"),
                "url": "",
            },
        ]

        for case in TEST_CASES:
            pk = get_thread_id_from_url(case["request"], case["url"])
            self.assertIsNone(
                pk, "get_thread_id_from_url for %s should fail" % case["url"]
            )
