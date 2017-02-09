from django.test import TestCase

from misago.threads.paginator import PostsPaginator


class PostsPaginatorTests(TestCase):
    def test_paginator(self):
        """pages share first and last items with each other"""
        items = [i + 1 for i in range(30)]

        paginator = PostsPaginator(items, 5)
        self.assertEqual(paginator.num_pages, 8)

        self.assertEqual(paginator.page(1).object_list, [1, 2, 3, 4, 5])
        self.assertEqual(paginator.page(2).object_list, [5, 6, 7, 8, 9])
        self.assertEqual(paginator.page(3).object_list, [9, 10, 11, 12, 13])
        self.assertEqual(paginator.page(4).object_list, [13, 14, 15, 16, 17])
        self.assertEqual(paginator.page(5).object_list, [17, 18, 19, 20, 21])
        self.assertEqual(paginator.page(6).object_list, [21, 22, 23, 24, 25])
        self.assertEqual(paginator.page(7).object_list, [25, 26, 27, 28, 29])
        self.assertEqual(paginator.page(8).object_list, [29, 30])

    def test_paginator_orphans(self):
        """paginator handles orphans"""
        items = [i + 1 for i in range(20)]

        paginator = PostsPaginator(items, 8, 6)
        self.assertEqual(paginator.num_pages, 2)

        self.assertEqual(
            paginator.page(1).object_list, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(
            paginator.page(2).object_list,
            [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

        paginator = PostsPaginator(items, 8, 4)
        self.assertEqual(paginator.num_pages, 3)

        self.assertEqual(
            paginator.page(1).object_list, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(
            paginator.page(2).object_list, [8, 9, 10, 11, 12, 13, 14, 15])
        self.assertEqual(
            paginator.page(3).object_list, [15, 16, 17, 18, 19, 20])

        paginator = PostsPaginator(items, 8, 6)
        self.assertEqual(paginator.num_pages, 2)

        self.assertEqual(
            paginator.page(1).object_list, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(
            paginator.page(2).object_list,
            [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

        paginator = PostsPaginator(items, 6, 5)
        self.assertEqual(paginator.num_pages, 3)

        self.assertEqual(paginator.page(1).object_list, [1, 2, 3, 4, 5, 6])
        self.assertEqual(paginator.page(2).object_list, [6, 7, 8, 9, 10, 11])
        self.assertEqual(
            paginator.page(3).object_list,
            [11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
