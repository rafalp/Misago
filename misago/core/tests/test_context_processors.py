from django.test import TestCase

from .. import context_processors


class MockRequest(object):
    path_info = '/'

    def __init__(self, secure, host):
        self.secure = secure
        self.host = host

    def is_secure(self):
        return self.secure

    def get_host(self):
        return self.host


class MetaMockRequest(object):
    def __init__(self, meta):
        self.META = meta


class SiteAddressTests(TestCase):
    def test_site_address_for_http(self):
        """Correct SITE_ADDRESS set for HTTP request"""
        mock_request = MockRequest(False, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(mock_request),
            {
                'REQUEST_PATH': '/',
                'SITE_ADDRESS': 'http://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'http',
            })

    def test_site_address_for_https(self):
        """Correct SITE_ADDRESS set for HTTPS request"""
        mock_request = MockRequest(True, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(mock_request),
            {
                'REQUEST_PATH': '/',
                'SITE_ADDRESS': 'https://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'https',
            })


class InternetExplorerTests(TestCase):
    def test_internet_explorer(self):
        """frontend_context returns true if user agent contains 'Trident/'"""
        IE_USERAGENTS = (
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)',
            'Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko',
            'Mozilla/5.0 (IE 11.0; Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        )

        NONIE_USERAGENTS = (
            'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36 Edge/12.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.9600',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10547',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 Edge/14.14359',
            'Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3',
            'Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5',
            'Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2',
            'Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1',
            'Mozilla/5.0 (Linux; Android 4.1; Galaxy Nexus Build/JRN84D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
            'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
            'Mozilla/5.0 (iPad; U; CPU OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
            'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/55.0.2883.79 Mobile/14C92 Safari/602.1',
            'Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A5376e',
        )

        for useragent in IE_USERAGENTS:
            context = context_processors.internet_explorer(MetaMockRequest({
                'HTTP_USER_AGENT': useragent
            }))

            self.assertEqual(context, {'is_ie': True})

        for useragent in NONIE_USERAGENTS:
            context = context_processors.internet_explorer(MetaMockRequest({
                'HTTP_USER_AGENT': useragent
            }))

            self.assertEqual(context, {'is_ie': False})

    def test_no_useragent(self):
        """no user agent causes no error"""
        context = context_processors.internet_explorer(MetaMockRequest({}))
        self.assertEqual(context, {'is_ie': False})

    def test_empty_useragent(self):
        """empty user agent causes no error"""
        context = context_processors.internet_explorer(MetaMockRequest({
            'HTTP_USER_AGENT': ''
        }))

        self.assertEqual(context, {'is_ie': False})


class FrontendContextTests(TestCase):
    def test_frontend_context(self):
        """frontend_context is available in templates"""
        mock_request = MockRequest(False, 'somewhere.com')
        mock_request.include_frontend_context = True
        mock_request.frontend_context = {'someValue': 'Something'}

        self.assertEqual(
            context_processors.frontend_context(mock_request),
            {'frontend_context': {'someValue': 'Something'}})

        mock_request.include_frontend_context = False
        self.assertEqual(context_processors.frontend_context(mock_request), {})
