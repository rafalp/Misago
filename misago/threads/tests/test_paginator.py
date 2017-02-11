from django.test import TestCase

from misago.threads.paginator import PostsPaginator


class PostsPaginatorTests(TestCase):
    def test_paginator(self):
        """pages share first and last items with each other"""
        items = [i + 1 for i in range(30)]

        paginator = PostsPaginator(items, 5)
        self.assertEqual(self.get_paginator_items_list(paginator), [
            [1, 2, 3, 4, 5, 6],
            [6, 7, 8, 9, 10, 11],
            [11, 12, 13, 14, 15, 16],
            [16, 17, 18, 19, 20, 21],
            [21, 22, 23, 24, 25, 26],
            [26, 27, 28, 29, 30],
        ])

    def test_paginator_orphans(self):
        """paginator handles orphans"""
        items = [i + 1 for i in range(20)]

        paginator = PostsPaginator(items, 8, 6)
        self.assertEqual(self.get_paginator_items_list(paginator), [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        ])

        paginator = PostsPaginator(items, 8, 5)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(self.get_paginator_items_list(paginator), [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        ])

        paginator = PostsPaginator(items, 9, 3)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(self.get_paginator_items_list(paginator), [
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        ])

        # regression test for #732
        items = [i + 1 for i in range(24)]

        paginator = PostsPaginator(items, 18, 6)
        self.assertEqual(paginator.num_pages, 1)
        self.assertEqual(self.get_paginator_items_list(paginator), [
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
        ])

        # extra tests for catching issues in excessively long datasets
        paginator = PostsPaginator([i + 1 for i in range(144)], 14, 6)
        last_page = self.get_paginator_items_list(paginator)[-1]
        self.assertEqual(last_page[-4:], [141, 142, 143, 144])

        paginator = PostsPaginator([i + 1 for i in range(321)], 14, 6)
        last_page = self.get_paginator_items_list(paginator)[-1]
        self.assertEqual(last_page[-4:], [318, 319, 320, 321])

    def get_paginator_items_list(self, paginator):
        items_list = []
        for page in paginator.page_range:
            items_list.append(paginator.page(page).object_list)
        return items_list
