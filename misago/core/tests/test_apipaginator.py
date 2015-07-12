from django.test import TestCase
from misago.core.apipaginator import ApiPaginator


class MockRequest(object):
    def __init__(self, page=None):
        self.query_params = {}
        if page:
            self.query_params['page'] = page


class PaginatorTests(TestCase):
    def test_init_paginator(self):
        """ApiPaginator returns type that can be initalized"""
        paginator = ApiPaginator(3, 1)()

    def test_empty_queryset(self):
        """pagination works for empty queryset"""
        paginator = ApiPaginator(6, 2)()
        querset = []

        results = paginator.paginate_queryset(querset, MockRequest())
        self.assertEqual(results, [])

        meta = paginator.get_meta()
        self.assertEqual(meta['count'], 0)
        self.assertEqual(meta['pages'], 1)
        self.assertEqual(meta['first'], None)
        self.assertEqual(meta['previous'], None)
        self.assertEqual(meta['next'], None)
        self.assertEqual(meta['last'], None)

    def test_first_page(self):
        """pagination works for first page of queryset"""
        paginator = ApiPaginator(6, 2)()
        querset = [i for i in xrange(20)]

        results = paginator.paginate_queryset(querset, MockRequest())
        self.assertEqual(results, [0, 1, 2, 3, 4, 5])

        meta = paginator.get_meta()
        self.assertEqual(meta['count'], 20)
        self.assertEqual(meta['pages'], 3)
        self.assertEqual(meta['first'], None)
        self.assertEqual(meta['previous'], None)
        self.assertEqual(meta['next'], 2)
        self.assertEqual(meta['last'], 3)

        response = paginator.get_paginated_response(results)
        self.assertEqual(response.status_code, 200)

    def test_next_page(self):
        """pagination works for next page of queryset"""
        paginator = ApiPaginator(6, 2)()
        querset = [i for i in xrange(20)]

        results = paginator.paginate_queryset(querset, MockRequest(2))
        self.assertEqual(results, [6, 7, 8, 9, 10, 11])

        meta = paginator.get_meta()
        self.assertEqual(meta['count'], 20)
        self.assertEqual(meta['pages'], 3)
        self.assertEqual(meta['first'], 1)
        self.assertEqual(meta['previous'], None)
        self.assertEqual(meta['next'], None)
        self.assertEqual(meta['last'], 3)

        response = paginator.get_paginated_response(results)
        self.assertEqual(response.status_code, 200)

    def test_last_page(self):
        """pagination works for next page of queryset"""
        paginator = ApiPaginator(6, 2)()
        querset = [i for i in xrange(20)]

        results = paginator.paginate_queryset(querset, MockRequest(3))
        self.assertEqual(results, [12, 13, 14, 15, 16, 17, 18, 19])

        meta = paginator.get_meta()
        self.assertEqual(meta['count'], 20)
        self.assertEqual(meta['pages'], 3)
        self.assertEqual(meta['first'], 1)
        self.assertEqual(meta['previous'], 2)
        self.assertEqual(meta['next'], None)
        self.assertEqual(meta['last'], None)

        response = paginator.get_paginated_response(results)
        self.assertEqual(response.status_code, 200)
