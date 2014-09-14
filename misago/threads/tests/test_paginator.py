from django.test import TestCase

from misago.threads.paginator import Paginator


class PaginatorTests(TestCase):
    def test_paginator_page_orphas(self):
        """paginator.page() returns orphans"""
        items = range(10)

        paginator = Paginator(items, 7, orphans=5)
        page = paginator.page(1)

        self.assertEqual(page.object_list, items)
        self.assertIsNone(page.next_page_first_item)

    def test_paginator_page_look_ahead(self):
        """paginator.page() has lookahead"""
        items = range(10)

        paginator = Paginator(items, 6, orphans=3)
        page = paginator.page(1)

        self.assertEqual(page.object_list, items[:6])
        self.assertEqual(page.next_page_first_item, items[6])

        page = paginator.page(2)
        self.assertEqual(page.object_list, items[6:])
        self.assertIsNone(page.next_page_first_item)
