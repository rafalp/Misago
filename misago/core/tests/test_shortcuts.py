from django.http import Http404
from django.test import TestCase, override_settings
from django.urls import reverse

from misago.core.shortcuts import get_int_or_404


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class PaginateTests(TestCase):
    def test_valid_page_handling(self):
        """Valid page number causes no errors"""
        response = self.client.get(reverse('test-pagination', kwargs={'page': 2}))
        self.assertEqual("5,6,7,8,9", response.content.decode())

    def test_invalid_page_handling(self):
        """Invalid page number results in 404 error"""
        response = self.client.get(reverse('test-pagination', kwargs={'page': 42}))
        self.assertEqual(response.status_code, 404)

    def test_implicit_page_handling(self):
        """Implicit page number causes no errors"""
        response = self.client.get(reverse('test-pagination'))
        self.assertEqual("0,1,2,3,4", response.content.decode())

    def test_explicit_page_handling(self):
        """Explicit page number results in redirect"""
        response = self.client.get(reverse('test-pagination', kwargs={'page': 1}))
        valid_url = "/forum/test-pagination/"
        self.assertEqual(response['Location'], valid_url)


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class ValidateSlugTests(TestCase):
    def test_valid_slug_handling(self):
        """Valid slug causes no interruption in view processing"""
        response = self.client.get(
            reverse('validate-slug-view', kwargs={
                'slug': 'eric-the-fish',
                'pk': 1,
            })
        )
        self.assertContains(response, "Allright")

    def test_invalid_slug_handling(self):
        """Invalid slug returns in redirect to valid page"""
        response = self.client.get(
            reverse('validate-slug-view', kwargs={
                'slug': 'lion-the-eric',
                'pk': 1,
            })
        )

        valid_url = "/forum/test-valid-slug/eric-the-fish-1/"
        self.assertEqual(response['Location'], valid_url)


class GetIntOr404Tests(TestCase):
    def test_valid_inputs(self):
        """get_int_or_404 returns int for valid values"""
        VALID_VALUES = [
            ('0', 0),
            ('123', 123),
            ('000123', 123),
            ('1', 1),
        ]

        for value, result in VALID_VALUES:
            self.assertEqual(get_int_or_404(value), result)

    def test_invalid_inputs(self):
        """get_int_or_404 raises Http404 for invalid values"""
        INVALID_VALUES = [
            None,
            '',
            'bob',
            '1bob',
            'b0b',
            'bob123',
            '12.321',
            '.4',
            '5.',
        ]

        for value in INVALID_VALUES:
            with self.assertRaises(Http404):
                get_int_or_404(value)


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class PaginatedResponseTests(TestCase):
    def test_page_response(self):
        """utility returns response for only page arg"""
        response = self.client.get(reverse('test-paginated-response'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'results': [i + 10 for i in range(10)],
                'page': 2,
                'pages': 10,
                'count': 100,
                'first': 1,
                'previous': 1,
                'next': 3,
                'last': 10,
                'before': 10,
                'more': 80,
            }
        )

    def test_explicit_data_response(self):
        """utility returns response with explicit data"""
        response = self.client.get(reverse('test-paginated-response-data'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'results': ['a', 'b', 'c', 'd', 'e'],
                'page': 2,
                'pages': 10,
                'count': 100,
                'first': 1,
                'previous': 1,
                'next': 3,
                'last': 10,
                'before': 10,
                'more': 80,
            }
        )

    def test_explicit_serializer_response(self):
        """utility returns response with data serialized via serializer"""
        response = self.client.get(reverse('test-paginated-response-serializer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'results': [
                    {
                        'id': 0
                    },
                    {
                        'id': 2
                    },
                    {
                        'id': 4
                    },
                    {
                        'id': 6
                    },
                ],
                'page': 1,
                'pages': 1,
                'count': 4,
                'first': None,
                'previous': None,
                'next': None,
                'last': None,
                'before': 0,
                'more': 0,
            }
        )

    def test_explicit_data_serializer_response(self):
        """utility returns response with explicit data serialized via serializer"""
        response = self.client.get(reverse('test-paginated-response-data-serializer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'results': [
                    {
                        'id': 'aa'
                    },
                    {
                        'id': 'bb'
                    },
                    {
                        'id': 'cc'
                    },
                    {
                        'id': 'dd'
                    },
                ],
                'page': 1,
                'pages': 1,
                'count': 4,
                'first': None,
                'previous': None,
                'next': None,
                'last': None,
                'before': 0,
                'more': 0,
            }
        )

    def test_explicit_data_extra_response(self):
        """utility returns response with explicit data and extra"""
        response = self.client.get(reverse('test-paginated-response-data-extra'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'results': ['a', 'b', 'c', 'd'],
                'page': 1,
                'pages': 1,
                'count': 4,
                'first': None,
                'previous': None,
                'next': 'EXTRA',
                'last': None,
                'before': 0,
                'more': 0,
                'lorem': 'ipsum'
            }
        )
