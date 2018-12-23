from itertools import product

from django.test import TestCase

from ..paginator import PostsPaginator


class PostsPaginatorTests(TestCase):
    def test_paginator(self):
        """pages share first and last items with each other"""
        items = [i + 1 for i in range(30)]

        paginator = PostsPaginator(items, 5)
        self.assertEqual(
            self.get_paginator_items_list(paginator),
            [
                [1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9],
                [9, 10, 11, 12, 13],
                [13, 14, 15, 16, 17],
                [17, 18, 19, 20, 21],
                [21, 22, 23, 24, 25],
                [25, 26, 27, 28, 29],
                [29, 30],
            ],
        )

    def test_paginator_orphans(self):
        """paginator handles orphans"""
        items = [i + 1 for i in range(16)]

        paginator = PostsPaginator(items, 8, 6)
        self.assertEqual(
            self.get_paginator_items_list(paginator),
            [[1, 2, 3, 4, 5, 6, 7, 8], [8, 9, 10, 11, 12, 13, 14, 15, 16]],
        )

        paginator = PostsPaginator(items, 4, 4)
        self.assertEqual(
            self.get_paginator_items_list(paginator),
            [[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10], [10, 11, 12, 13, 14, 15, 16]],
        )

        paginator = PostsPaginator(items, 5, 3)
        self.assertEqual(
            self.get_paginator_items_list(paginator),
            [[1, 2, 3, 4, 5], [5, 6, 7, 8, 9], [9, 10, 11, 12, 13, 14, 15, 16]],
        )

        paginator = PostsPaginator(items, 6, 2)
        self.assertEqual(
            self.get_paginator_items_list(paginator),
            [[1, 2, 3, 4, 5, 6], [6, 7, 8, 9, 10, 11], [11, 12, 13, 14, 15, 16]],
        )

        paginator = PostsPaginator(items, 7, 1)
        self.assertEqual(
            self.get_paginator_items_list(paginator),
            [[1, 2, 3, 4, 5, 6, 7], [7, 8, 9, 10, 11, 12, 13], [13, 14, 15, 16]],
        )

        paginator = PostsPaginator(items, 7, 3)
        self.assertEqual(
            self.get_paginator_items_list(paginator),
            [[1, 2, 3, 4, 5, 6, 7], [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]],
        )

        paginator = PostsPaginator(items, 10, 6)
        self.assertEqual(self.get_paginator_items_list(paginator), [items])

    def test_paginator_overlap(self):
        """test for #732 - assert that page contants don't overlap too much"""
        num_items = 16
        items = [i + 1 for i in range(num_items)]

        for per_page, orphans in product(range(num_items), range(num_items)):
            paginator = PostsPaginator(items, per_page + 2, orphans)
            pages = self.get_paginator_items_list(paginator)
            for p, page in enumerate(pages):
                for c, compared in enumerate(pages):
                    if p == c:
                        continue

                    common_part = set(page) & set(compared)
                    self.assertTrue(
                        len(common_part) < 2,
                        "invalid page %s: %s"
                        % (max(p, c) + 1, sorted(list(common_part))),
                    )

    def get_paginator_items_list(self, paginator):
        items_list = []
        for page in paginator.page_range:
            items_list.append(paginator.page(page).object_list)
        return items_list
