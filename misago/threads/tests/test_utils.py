from django.test import TestCase

from .. import test
from ...categories.models import Category
from ..utils import add_categories_to_items, get_thread_id_from_url


class AddCategoriesToItemsTests(TestCase):
    def setUp(self):
        """
        Create categories tree for test cases:

        First category (created by migration)

        Category A
          + Category B
            + Subcategory C
            + Subcategory D

        Category E
          + Subcategory F
        """
        super().setUp()

        self.root = Category.objects.root_category()

        Category(
            name="Category A", slug="category-a", css_class="showing-category-a"
        ).insert_at(self.root, position="last-child", save=True)
        Category(
            name="Category E", slug="category-e", css_class="showing-category-e"
        ).insert_at(self.root, position="last-child", save=True)

        self.root = Category.objects.root_category()

        self.category_a = Category.objects.get(slug="category-a")
        Category(
            name="Category B", slug="category-b", css_class="showing-category-b"
        ).insert_at(self.category_a, position="last-child", save=True)

        self.category_b = Category.objects.get(slug="category-b")
        Category(
            name="Category C", slug="category-c", css_class="showing-category-c"
        ).insert_at(self.category_b, position="last-child", save=True)
        Category(
            name="Category D", slug="category-d", css_class="showing-category-d"
        ).insert_at(self.category_b, position="last-child", save=True)

        self.category_c = Category.objects.get(slug="category-c")
        self.category_d = Category.objects.get(slug="category-d")

        self.category_e = Category.objects.get(slug="category-e")
        Category(
            name="Category F", slug="category-f", css_class="showing-category-f"
        ).insert_at(self.category_e, position="last-child", save=True)

        Category.objects.partial_rebuild(self.root.tree_id)

        self.root = Category.objects.root_category()
        self.category_a = Category.objects.get(slug="category-a")
        self.category_b = Category.objects.get(slug="category-b")
        self.category_c = Category.objects.get(slug="category-c")
        self.category_d = Category.objects.get(slug="category-d")
        self.category_e = Category.objects.get(slug="category-e")
        self.category_f = Category.objects.get(slug="category-f")

        self.categories = list(Category.objects.all_categories(include_root=True))

    def test_root_thread_from_root(self):
        """thread in root category is handled"""
        thread = test.post_thread(category=self.root)
        add_categories_to_items(self.root, self.categories, [thread])

        self.assertEqual(thread.category, self.root)

    def test_root_thread_from_elsewhere(self):
        """thread in root category is handled"""
        thread = test.post_thread(category=self.root)
        add_categories_to_items(self.category_e, self.categories, [thread])

        self.assertEqual(thread.category, self.root)

    def test_direct_child_thread_from_parent(self):
        """thread in direct child category is handled"""
        thread = test.post_thread(category=self.category_e)
        add_categories_to_items(self.root, self.categories, [thread])

        self.assertEqual(thread.category, self.category_e)

    def test_direct_child_thread_from_elsewhere(self):
        """thread in direct child category is handled"""
        thread = test.post_thread(category=self.category_e)
        add_categories_to_items(self.category_b, self.categories, [thread])

        self.assertEqual(thread.category, self.category_e)

    def test_child_thread_from_root(self):
        """thread in child category is handled"""
        thread = test.post_thread(category=self.category_d)
        add_categories_to_items(self.root, self.categories, [thread])

        self.assertEqual(thread.category, self.category_d)

    def test_child_thread_from_parent(self):
        """thread in child category is handled"""
        thread = test.post_thread(category=self.category_d)
        add_categories_to_items(self.category_a, self.categories, [thread])

        self.assertEqual(thread.category, self.category_d)

    def test_child_thread_from_category(self):
        """thread in child category is handled"""
        thread = test.post_thread(category=self.category_d)
        add_categories_to_items(self.category_d, self.categories, [thread])

        self.assertEqual(thread.category, self.category_d)

    def test_child_thread_from_elsewhere(self):
        """thread in child category is handled"""
        thread = test.post_thread(category=self.category_d)
        add_categories_to_items(self.category_f, self.categories, [thread])

        self.assertEqual(thread.category, self.category_d)


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
