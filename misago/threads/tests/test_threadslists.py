from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_str

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.conf import settings
from misago.readtracker import threadstracker
from misago.threads import testutils
from misago.users.models import AnonymousUser
from misago.users.testutils import AuthenticatedUserTestCase


LISTS_URLS = ('', 'my/', 'new/', 'unread/', 'subscribed/', )


class ThreadsListTestCase(AuthenticatedUserTestCase):
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
        super(ThreadsListTestCase, self).setUp()

        self.api_link = reverse('misago:api:thread-list')

        self.root = Category.objects.root_category()
        self.first_category = Category.objects.get(slug='first-category')

        Category(
            name='Category A',
            slug='category-a',
            css_class='showing-category-a',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )
        Category(
            name='Category E',
            slug='category-e',
            css_class='showing-category-e',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )

        self.root = Category.objects.root_category()

        self.category_a = Category.objects.get(slug='category-a')

        Category(
            name='Category B',
            slug='category-b',
            css_class='showing-category-b',
        ).insert_at(
            self.category_a,
            position='last-child',
            save=True,
        )

        self.category_b = Category.objects.get(slug='category-b')

        Category(
            name='Category C',
            slug='category-c',
            css_class='showing-category-c',
        ).insert_at(
            self.category_b,
            position='last-child',
            save=True,
        )
        Category(
            name='Category D',
            slug='category-d',
            css_class='showing-category-d',
        ).insert_at(
            self.category_b,
            position='last-child',
            save=True,
        )

        self.category_c = Category.objects.get(slug='category-c')
        self.category_d = Category.objects.get(slug='category-d')

        self.category_e = Category.objects.get(slug='category-e')
        Category(
            name='Category F',
            slug='category-f',
            css_class='showing-category-f',
        ).insert_at(
            self.category_e,
            position='last-child',
            save=True,
        )

        self.category_f = Category.objects.get(slug='category-f')

        self.clear_state()

        Category.objects.partial_rebuild(self.root.tree_id)

        self.root = Category.objects.root_category()
        self.category_a = Category.objects.get(slug='category-a')
        self.category_b = Category.objects.get(slug='category-b')
        self.category_c = Category.objects.get(slug='category-c')
        self.category_d = Category.objects.get(slug='category-d')
        self.category_e = Category.objects.get(slug='category-e')
        self.category_f = Category.objects.get(slug='category-f')

        self.access_all_categories()

    def access_all_categories(self, category_acl=None, base_acl=None):
        self.clear_state()

        categories_acl = {
            'categories': {},
            'visible_categories': [],
            'browseable_categories': [],
            'can_approve_content': [],
        }

        # copy first category's acl to other categories to make base for overrides
        first_category_acl = self.user.acl_cache['categories'][self.first_category.pk].copy()
        for category in Category.objects.all_categories():
            categories_acl['categories'][category.pk] = first_category_acl

        if base_acl:
            categories_acl.update(base_acl)

        for category in Category.objects.all_categories():
            categories_acl['visible_categories'].append(category.pk)
            categories_acl['browseable_categories'].append(category.pk)
            categories_acl['categories'][category.pk].update({
                'can_see': 1,
                'can_browse': 1,
                'can_see_all_threads': 1,
                'can_see_own_threads': 0,
                'can_hide_threads': 0,
                'can_approve_content': 0,
            })

            if category_acl:
                categories_acl['categories'][category.pk].update(category_acl)
                if category_acl.get('can_approve_content'):
                    categories_acl['can_approve_content'].append(category.pk)

        override_acl(self.user, categories_acl)
        return categories_acl

    def assertContainsThread(self, response, thread):
        self.assertContains(response, u' href="{}"'.format(thread.get_absolute_url()))

    def assertNotContainsThread(self, response, thread):
        self.assertNotContains(response, u' href="{}"'.format(thread.get_absolute_url()))


class ApiTests(ThreadsListTestCase):
    def test_root_category(self):
        """its possible to access threads endpoint with category=ROOT_ID"""
        response = self.client.get('%s?category=%s' % (self.api_link, self.root.pk, ))
        self.assertEqual(response.status_code, 200)

    def test_explicit_first_page(self):
        """its possible to access threads endpoint with explicit first page"""
        response = self.client.get('%s?category=%s&page=1' % (self.api_link, self.root.pk, ))
        self.assertEqual(response.status_code, 200)

    def test_invalid_list_type(self):
        """api returns 404 for invalid list type"""
        response = self.client.get('%s?category=%s&list=nope' % (self.api_link, self.root.pk, ))
        self.assertEqual(response.status_code, 404)


class AllThreadsListTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """empty threads list renders"""
        for url in LISTS_URLS:
            self.access_all_categories()

            response = self.client.get('/' + url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "empty-message")

            self.access_all_categories()

            response = self.client.get(self.category_b.get_absolute_url() + url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.category_b.name)
            self.assertContains(response, "empty-message")

            self.access_all_categories()

            response = self.client.get('%s?list=%s' % (self.api_link, url.strip('/') or 'all'))
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertEqual(len(response_json['results']), 0)

    def test_list_authenticated_only_views(self):
        """authenticated only views return 403 for guests"""
        for url in LISTS_URLS:
            self.access_all_categories()

            response = self.client.get('/' + url)
            self.assertEqual(response.status_code, 200)

            self.access_all_categories()

            response = self.client.get(self.category_b.get_absolute_url() + url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.category_b.name)

            self.access_all_categories()

            self.access_all_categories()
            response = self.client.get(
                '%s?category=%s&list=%s' %
                (self.api_link, self.category_b.pk, url.strip('/') or 'all', )
            )
            self.assertEqual(response.status_code, 200)

        self.logout_user()
        self.user = self.get_anonymous_user()
        for url in LISTS_URLS[1:]:
            self.access_all_categories()

            response = self.client.get('/' + url)
            self.assertEqual(response.status_code, 403)

            self.access_all_categories()
            response = self.client.get(self.category_b.get_absolute_url() + url)
            self.assertEqual(response.status_code, 403)

            self.access_all_categories()
            response = self.client.get(
                '%s?category=%s&list=%s' %
                (self.api_link, self.category_b.pk, url.strip('/') or 'all', )
            )
            self.assertEqual(response.status_code, 403)

    def test_list_renders_categories_picker(self):
        """categories picker renders valid categories"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )
        test_category = Category.objects.get(slug='hidden-category')

        testutils.post_thread(
            category=self.category_b,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'subcategory-%s' % self.category_a.css_class)

        # readable categories, but non-accessible directly
        self.assertNotContains(response, 'subcategory-%s' % self.category_b.css_class)
        self.assertNotContains(response, 'subcategory-%s' % self.category_c.css_class)
        self.assertNotContains(response, 'subcategory-%s' % self.category_d.css_class)
        self.assertNotContains(response, 'subcategory-%s' % self.category_f.css_class)

        # hidden category
        self.assertNotContains(response, 'subcategory-%s' % test_category.css_class)

        self.access_all_categories()
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIn(self.category_a.pk, response_json['subcategories'])
        self.assertNotIn(self.category_b.pk, response_json['subcategories'])

        # test category view
        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'subcategory-%s' % self.category_b.css_class)

        # readable categories, but non-accessible directly
        self.assertNotContains(response, 'subcategory-%s' % self.category_c.css_class)
        self.assertNotContains(response, 'subcategory-%s' % self.category_d.css_class)
        self.assertNotContains(response, 'subcategory-%s' % self.category_f.css_class)

        self.access_all_categories()
        response = self.client.get('%s?category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['subcategories'][0], self.category_b.pk)

    def test_display_pinned_threads(self):
        """
        threads list displays globally pinned threads first
        and locally ones inbetween other
        """
        globally = testutils.post_thread(
            category=self.first_category,
            is_global=True,
        )

        locally = testutils.post_thread(
            category=self.first_category,
            is_pinned=True,
        )

        standard = testutils.post_thread(category=self.first_category)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        content = smart_str(response.content)
        positions = {
            'g': content.find(globally.get_absolute_url()),
            'l': content.find(locally.get_absolute_url()),
            's': content.find(standard.get_absolute_url()),
        }

        # global announcement before others
        self.assertTrue(positions['g'] < positions['l'])
        self.assertTrue(positions['g'] < positions['s'])

        # standard in the middle
        self.assertTrue(positions['s'] < positions['l'])
        self.assertTrue(positions['s'] > positions['g'])

        # pinned last
        self.assertTrue(positions['l'] > positions['g'])
        self.assertTrue(positions['l'] > positions['s'])

        # API behaviour is identic
        response = self.client.get('/api/threads/')
        self.assertEqual(response.status_code, 200)

        content = smart_str(response.content)
        positions = {
            'g': content.find(globally.get_absolute_url()),
            'l': content.find(locally.get_absolute_url()),
            's': content.find(standard.get_absolute_url()),
        }

        # global announcement before others
        self.assertTrue(positions['g'] < positions['l'])
        self.assertTrue(positions['g'] < positions['s'])

        # standard in the middle
        self.assertTrue(positions['s'] < positions['l'])
        self.assertTrue(positions['s'] > positions['g'])

        # pinned last
        self.assertTrue(positions['l'] > positions['g'])
        self.assertTrue(positions['l'] > positions['s'])

    def test_noscript_pagination(self):
        """threads list is paginated for users with js disabled"""
        threads_per_page = settings.MISAGO_THREADS_PER_PAGE

        threads = []
        for _ in range(settings.MISAGO_THREADS_PER_PAGE * 3):
            threads.append(testutils.post_thread(category=self.first_category))

        # secondary page renders
        response = self.client.get('/?page=2')
        self.assertEqual(response.status_code, 200)

        for thread in threads[:threads_per_page]:
            self.assertNotContainsThread(response, thread)
        for thread in threads[threads_per_page:threads_per_page * 2]:
            self.assertContainsThread(response, thread)
        for thread in threads[threads_per_page * 2:]:
            self.assertNotContainsThread(response, thread)

        self.assertNotContains(response, '/?page=1')
        self.assertContains(response, '/?page=3')

        # third page renders
        response = self.client.get('/?page=3')
        self.assertEqual(response.status_code, 200)

        for thread in threads[threads_per_page:]:
            self.assertNotContainsThread(response, thread)
        for thread in threads[:threads_per_page]:
            self.assertContainsThread(response, thread)

        self.assertContains(response, '/?page=2')
        self.assertNotContains(response, '/?page=4')

        # excessive page gives 404
        response = self.client.get('/?page=4')
        self.assertEqual(response.status_code, 404)


class CategoryThreadsListTests(ThreadsListTestCase):
    def test_access_hidden_category(self):
        """hidden category returns 404"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )
        test_category = Category.objects.get(slug='hidden-category')

        for url in LISTS_URLS:
            response = self.client.get(test_category.get_absolute_url() + url)
            self.assertEqual(response.status_code, 404)

            response = self.client.get('%s?category=%s' % (self.api_link, test_category.pk))
            self.assertEqual(response.status_code, 404)

    def test_access_protected_category(self):
        """protected category returns 403"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )
        test_category = Category.objects.get(slug='hidden-category')

        for url in LISTS_URLS:
            override_acl(
                self.user, {
                    'visible_categories': [test_category.pk],
                    'browseable_categories': [test_category.pk],
                    'categories': {
                        test_category.pk: {
                            'can_see': 1,
                            'can_browse': 0,
                        },
                    },
                }
            )

            response = self.client.get(test_category.get_absolute_url() + url)
            self.assertEqual(response.status_code, 403)

            override_acl(
                self.user, {
                    'visible_categories': [test_category.pk],
                    'browseable_categories': [test_category.pk],
                    'categories': {
                        test_category.pk: {
                            'can_see': 1,
                            'can_browse': 0,
                        },
                    },
                }
            )

            response = self.client.get(
                '%s?category=%s&list=%s' % (self.api_link, test_category.pk, url.strip('/'), )
            )
            self.assertEqual(response.status_code, 403)

    def test_display_pinned_threads(self):
        """
        category threads list displays globally pinned threads first
        then locally ones and unpinned last
        """
        globally = testutils.post_thread(
            category=self.first_category,
            is_global=True,
        )

        locally = testutils.post_thread(
            category=self.first_category,
            is_pinned=True,
        )

        standard = testutils.post_thread(category=self.first_category)

        response = self.client.get(self.first_category.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        content = smart_str(response.content)
        positions = {
            'g': content.find(globally.get_absolute_url()),
            'l': content.find(locally.get_absolute_url()),
            's': content.find(standard.get_absolute_url()),
        }

        # global announcement before others
        self.assertTrue(positions['g'] < positions['l'])
        self.assertTrue(positions['g'] < positions['s'])

        # pinned in the middle
        self.assertTrue(positions['l'] < positions['s'])
        self.assertTrue(positions['l'] > positions['g'])

        # standard last
        self.assertTrue(positions['s'] > positions['g'])
        self.assertTrue(positions['s'] > positions['g'])

        # API behaviour is identic
        response = self.client.get('/api/threads/?category=%s' % self.first_category.pk)
        self.assertEqual(response.status_code, 200)

        content = smart_str(response.content)
        positions = {
            'g': content.find(globally.get_absolute_url()),
            'l': content.find(locally.get_absolute_url()),
            's': content.find(standard.get_absolute_url()),
        }

        # global announcement before others
        self.assertTrue(positions['g'] < positions['l'])
        self.assertTrue(positions['g'] < positions['s'])

        # pinned in the middle
        self.assertTrue(positions['l'] < positions['s'])
        self.assertTrue(positions['l'] > positions['g'])

        # standard last
        self.assertTrue(positions['s'] > positions['g'])
        self.assertTrue(positions['s'] > positions['g'])


class ThreadsVisibilityTests(ThreadsListTestCase):
    def test_list_renders_test_thread(self):
        """list renders test thread with valid top category"""
        test_thread = testutils.post_thread(
            category=self.category_c,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertContainsThread(response, test_thread)

        self.assertContains(response, 'subcategory-%s' % self.category_a.css_class)
        self.assertContains(response, 'subcategory-%s' % self.category_e.css_class)

        self.assertNotContains(response, 'thread-detail-category-%s' % self.category_a.css_class)
        self.assertContains(response, 'thread-detail-category-%s' % self.category_c.css_class)

        # api displays same data
        self.access_all_categories()
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)
        self.assertEqual(len(response_json['subcategories']), 3)
        self.assertIn(self.category_a.pk, response_json['subcategories'])

        # test category view
        self.access_all_categories()
        response = self.client.get(self.category_b.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # thread displays
        self.assertContainsThread(response, test_thread)

        self.assertNotContains(response, 'thread-detail-category-%s' % self.category_b.css_class)
        self.assertContains(response, 'thread-detail-category-%s' % self.category_c.css_class)

        # api displays same data
        self.access_all_categories()
        response = self.client.get('%s?category=%s' % (self.api_link, self.category_b.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)
        self.assertEqual(len(response_json['subcategories']), 2)
        self.assertEqual(response_json['subcategories'][0], self.category_c.pk)

    def test_list_hides_hidden_thread(self):
        """list renders empty due to no permission to see thread"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )

        test_category = Category.objects.get(slug='hidden-category')
        test_thread = testutils.post_thread(category=test_category)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")
        self.assertNotContainsThread(response, test_thread)

    def test_api_hides_hidden_thread(self):
        """api returns empty due to no permission to see thread"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(
            self.root,
            position='last-child',
            save=True,
        )

        test_category = Category.objects.get(slug='hidden-category')

        testutils.post_thread(
            category=test_category,
        )

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_user_see_own_unapproved_thread(self):
        """list renders unapproved thread that belongs to viewer"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
            is_unapproved=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

    def test_list_user_cant_see_unapproved_thread(self):
        """list hides unapproved thread that belongs to other user"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_unapproved=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_user_cant_see_hidden_thread(self):
        """list hides hidden thread that belongs to other user"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_hidden=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_user_cant_see_own_hidden_thread(self):
        """list hides hidden thread that belongs to viewer"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
            is_hidden=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_user_can_see_own_hidden_thread(self):
        """list shows hidden thread that belongs to viewer due to permission"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
            is_hidden=True,
        )

        self.access_all_categories({'can_hide_threads': 1})

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories({'can_hide_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

    def test_list_user_can_see_hidden_thread(self):
        """list shows hidden thread that belongs to other user due to permission"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_hidden=True,
        )

        self.access_all_categories({'can_hide_threads': 1})

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories({'can_hide_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

    def test_list_user_can_see_unapproved_thread(self):
        """list shows hidden thread that belongs to other user due to permission"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_unapproved=True,
        )

        self.access_all_categories({'can_approve_content': 1})

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories({'can_approve_content': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)


class MyThreadsListTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """list renders empty"""
        self.access_all_categories()

        response = self.client.get('/my/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'my/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=my' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get('%s?list=my&category=%s' % (self.api_link, self.category_a.pk))

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_renders_test_thread(self):
        """list renders only threads posted by user"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
        )

        other_thread = testutils.post_thread(category=self.category_a)

        self.access_all_categories()

        response = self.client.get('/my/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)
        self.assertNotContainsThread(response, other_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'my/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)
        self.assertNotContainsThread(response, other_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=my' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

        self.access_all_categories()
        response = self.client.get('%s?list=my&category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)


class NewThreadsListTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """list renders empty"""
        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=new' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get('%s?list=new&category=%s' % (self.api_link, self.category_a.pk))

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_renders_new_thread(self):
        """list renders new thread"""
        test_thread = testutils.post_thread(category=self.category_a)

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=new' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

        self.access_all_categories()
        response = self.client.get('%s?list=new&category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

    def test_list_renders_thread_bumped_after_user_cutoff(self):
        """list renders new thread bumped after user cutoff"""
        self.user.joined_on = timezone.now() - timedelta(days=10)
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.joined_on - timedelta(days=2),
        )

        testutils.reply_thread(
            test_thread,
            posted_on=self.user.joined_on + timedelta(days=4),
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=new' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

        self.access_all_categories()
        response = self.client.get('%s?list=new&category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

    def test_list_hides_global_cutoff_thread(self):
        """list hides thread started before global cutoff"""
        self.user.joined_on = timezone.now() - timedelta(days=10)
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF + 1),
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=new' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get('%s?list=new&category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_hides_user_cutoff_thread(self):
        """list hides thread started before users cutoff"""
        self.user.joined_on = timezone.now() - timedelta(days=5)
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.joined_on - timedelta(minutes=1),
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=new' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get('%s?list=new&category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_hides_user_read_thread(self):
        """list hides thread already read by user"""
        self.user.joined_on = timezone.now() - timedelta(days=5)
        self.user.save()

        test_thread = testutils.post_thread(category=self.category_a)

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(self.user, test_thread, test_thread.last_post)

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=new' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get('%s?list=new&category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_hides_category_read_thread(self):
        """list hides thread already read by user"""
        self.user.joined_on = timezone.now() - timedelta(days=5)
        self.user.save()

        test_thread = testutils.post_thread(category=self.category_a)

        self.user.categoryread_set.create(
            category=self.category_a,
            last_read_on=timezone.now(),
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=new' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get('%s?list=new&category=%s' % (self.api_link, self.category_a.pk))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)


class UnreadThreadsListTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """list renders empty"""
        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=unread' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=unread&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_renders_unread_thread(self):
        """list renders thread with unread posts"""
        self.user.joined_on = timezone.now() - timedelta(days=5)
        self.user.save()

        test_thread = testutils.post_thread(category=self.category_a)

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(test_thread)

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=unread' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=unread&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertEqual(response_json['results'][0]['id'], test_thread.pk)

    def test_list_hides_never_read_thread(self):
        """list hides never read thread"""
        self.user.joined_on = timezone.now() - timedelta(days=5)
        self.user.save()

        test_thread = testutils.post_thread(category=self.category_a)

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=unread' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=unread&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_hides_read_thread(self):
        """list hides read thread"""
        self.user.joined_on = timezone.now() - timedelta(days=5)
        self.user.save()

        test_thread = testutils.post_thread(category=self.category_a)

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(self.user, test_thread, test_thread.last_post)

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=unread' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=unread&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_hides_global_cutoff_thread(self):
        """list hides thread replied before global cutoff"""
        self.user.joined_on = timezone.now() - timedelta(days=10)
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF + 5),
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(test_thread, posted_on=test_thread.started_on + timedelta(days=1))

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=unread' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=unread&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_hides_user_cutoff_thread(self):
        """list hides thread replied before user cutoff"""
        self.user.joined_on = timezone.now() - timedelta(days=10)
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.joined_on - timedelta(days=2),
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(
            test_thread,
            posted_on=test_thread.started_on + timedelta(days=1),
        )

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=unread' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=unread&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

    def test_list_hides_category_cutoff_thread(self):
        """list hides thread replied before category cutoff"""
        self.user.joined_on = timezone.now() - timedelta(days=10)
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.joined_on - timedelta(days=2),
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(test_thread)

        self.user.categoryread_set.create(
            category=self.category_a,
            last_read_on=timezone.now(),
        )

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=unread' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=unread&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)


class SubscribedThreadsListTests(ThreadsListTestCase):
    def test_list_shows_subscribed_thread(self):
        """list shows subscribed thread"""
        test_thread = testutils.post_thread(category=self.category_a)
        self.user.subscription_set.create(
            thread=test_thread,
            category=self.category_a,
            last_read_on=test_thread.last_post_on,
        )

        self.access_all_categories()

        response = self.client.get('/subscribed/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'subscribed/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=subscribed' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertContains(response, test_thread.get_absolute_url())

        self.access_all_categories()
        response = self.client.get(
            '%s?list=subscribed&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 1)
        self.assertContains(response, test_thread.get_absolute_url())

    def test_list_hides_unsubscribed_thread(self):
        """list shows subscribed thread"""
        test_thread = testutils.post_thread(category=self.category_a)

        self.access_all_categories()

        response = self.client.get('/subscribed/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'subscribed/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContainsThread(response, test_thread)

        # test api
        self.access_all_categories()
        response = self.client.get('%s?list=subscribed' % self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)
        self.assertNotContainsThread(response, test_thread)

        self.access_all_categories()
        response = self.client.get(
            '%s?list=subscribed&category=%s' % (self.api_link, self.category_a.pk)
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json['results']), 0)
        self.assertNotContainsThread(response, test_thread)


class UnapprovedListTests(ThreadsListTestCase):
    def test_list_errors_without_permission(self):
        """list errors if user has no permission to access it"""
        TEST_URLS = (
            '/unapproved/', self.category_a.get_absolute_url() + 'unapproved/',
            '%s?list=unapproved' % self.api_link,
        )

        for test_url in TEST_URLS:
            self.access_all_categories()
            response = self.client.get(test_url)
            self.assertEqual(response.status_code, 403)

        # approval perm has no influence on visibility
        for test_url in TEST_URLS:
            self.access_all_categories({'can_approve_content': True})

            self.access_all_categories()
            response = self.client.get(test_url)
            self.assertEqual(response.status_code, 403)

        # approval perm has no influence on visibility
        for test_url in TEST_URLS:
            self.access_all_categories(base_acl={
                'can_see_unapproved_content_lists': True,
            })

            self.access_all_categories()
            response = self.client.get(test_url)
            self.assertEqual(response.status_code, 200)

    def test_list_shows_all_threads_for_approving_user(self):
        """list shows all threads with unapproved posts when user has perm"""
        visible_thread = testutils.post_thread(
            category=self.category_b,
            is_unapproved=True,
        )

        hidden_thread = testutils.post_thread(
            category=self.category_b,
            is_unapproved=False,
        )

        self.access_all_categories({
            'can_approve_content': True,
        }, {
            'can_see_unapproved_content_lists': True,
        })

        response = self.client.get('/unapproved/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, visible_thread)
        self.assertNotContainsThread(response, hidden_thread)

        self.access_all_categories({
            'can_approve_content': True
        }, {
            'can_see_unapproved_content_lists': True,
        })

        response = self.client.get(self.category_a.get_absolute_url() + 'unapproved/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, visible_thread)
        self.assertNotContainsThread(response, hidden_thread)

        # test api
        self.access_all_categories({
            'can_approve_content': True
        }, {
            'can_see_unapproved_content_lists': True,
        })

        response = self.client.get('%s?list=unapproved' % self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, visible_thread.get_absolute_url())
        self.assertNotContains(response, hidden_thread.get_absolute_url())

    def test_list_shows_owned_threads_for_unapproving_user(self):
        """list shows owned threads with unapproved posts for user without perm"""
        visible_thread = testutils.post_thread(
            poster=self.user,
            category=self.category_b,
            is_unapproved=True,
        )

        hidden_thread = testutils.post_thread(
            category=self.category_b,
            is_unapproved=True,
        )

        self.access_all_categories(base_acl={
            'can_see_unapproved_content_lists': True,
        })
        response = self.client.get('/unapproved/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, visible_thread)
        self.assertNotContainsThread(response, hidden_thread)

        self.access_all_categories(base_acl={
            'can_see_unapproved_content_lists': True,
        })
        response = self.client.get(self.category_a.get_absolute_url() + 'unapproved/')
        self.assertEqual(response.status_code, 200)
        self.assertContainsThread(response, visible_thread)
        self.assertNotContainsThread(response, hidden_thread)

        # test api
        self.access_all_categories(base_acl={
            'can_see_unapproved_content_lists': True,
        })
        response = self.client.get('%s?list=unapproved' % self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, visible_thread.get_absolute_url())
        self.assertNotContains(response, hidden_thread.get_absolute_url())


class OwnerOnlyThreadsVisibilityTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(OwnerOnlyThreadsVisibilityTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')

    def override_acl(self, user):
        category_acl = user.acl_cache['categories'][self.category.pk].copy()
        category_acl.update({'can_see_all_threads': 0})
        user.acl_cache['categories'][self.category.pk] = category_acl

        override_acl(user, user.acl_cache)

    def test_owned_threads_visibility(self):
        """only user-posted threads are visible in category"""
        self.override_acl(self.user)

        visible_thread = testutils.post_thread(
            poster=self.user,
            category=self.category,
            is_unapproved=True,
        )

        hidden_thread = testutils.post_thread(
            category=self.category,
            is_unapproved=True,
        )

        response = self.client.get(self.category.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, visible_thread.get_absolute_url())
        self.assertNotContains(response, hidden_thread.get_absolute_url())

    def test_owned_threads_visibility_anonymous(self):
        """anons can't see any threads in limited visibility category"""
        self.logout_user()

        self.override_acl(AnonymousUser())

        user_thread = testutils.post_thread(
            poster=self.user,
            category=self.category,
            is_unapproved=True,
        )

        guest_thread = testutils.post_thread(
            category=self.category,
            is_unapproved=True,
        )

        response = self.client.get(self.category.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user_thread.get_absolute_url())
        self.assertNotContains(response, guest_thread.get_absolute_url())
