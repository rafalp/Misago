from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.core import threadstore
from misago.core.cache import cache
from misago.readtracker import categoriestracker, threadstracker
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import testutils


LISTS_URLS = (
    '',
    'my/',
    'new/',
    'unread/',
    'subscribed/'
)


class ThreadsListTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsListTestCase, self).setUp()

        cache.clear()
        threadstore.clear()

        self.root = Category.objects.root_category()
        self.first_category = Category.objects.get(slug='first-category')

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
        Category(
            name='Category A',
            slug='category-a',
            css_class='showing-category-a',
        ).insert_at(self.root, position='last-child', save=True)
        Category(
            name='Category E',
            slug='category-e',
            css_class='showing-category-e',
        ).insert_at(self.root, position='last-child', save=True)

        self.root = Category.objects.root_category()

        self.category_a = Category.objects.get(slug='category-a')

        Category(
            name='Category B',
            slug='category-b',
            css_class='showing-category-b',
        ).insert_at(self.category_a, position='last-child', save=True)

        self.category_b = Category.objects.get(slug='category-b')

        Category(
            name='Category C',
            slug='category-c',
            css_class='showing-category-c',
        ).insert_at(self.category_b, position='last-child', save=True)
        Category(
            name='Category D',
            slug='category-d',
            css_class='showing-category-d',
        ).insert_at(self.category_b, position='last-child', save=True)

        self.category_c = Category.objects.get(slug='category-c')
        self.category_d = Category.objects.get(slug='category-d')

        self.category_e = Category.objects.get(slug='category-e')
        Category(
            name='Category F',
            slug='category-f',
            css_class='showing-category-f',
        ).insert_at(self.category_e, position='last-child', save=True)

        self.category_f = Category.objects.get(slug='category-f')

        self.access_all_categories()

    def access_all_categories(self, extra=None):
        cache.clear()
        threadstore.clear()

        categories_acl = {'categories': {}, 'visible_categories': []}
        for category in Category.objects.all_categories():
            categories_acl['visible_categories'].append(category.pk)
            categories_acl['categories'][category.pk] = {
                'can_see': 1,
                'can_browse': 1,
                'can_see_all_threads': 1,
                'can_see_own_threads': 0,
                'can_hide_threads': 0,
                'can_review_moderated_content': 0,
            }

            if extra:
                categories_acl['categories'][category.pk].update(extra)

        override_acl(self.user, categories_acl)
        return categories_acl


class ListsTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """empty threads list renders"""
        for url in LISTS_URLS:
            self.access_all_categories()

            response = self.client.get('/' + url)
            self.assertEqual(response.status_code, 200)
            self.assertIn("empty-message", response.content)

            self.access_all_categories()

            response = self.client.get(self.category_b.get_absolute_url() + url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.category_b.name, response.content)
            self.assertIn("empty-message", response.content)

    def test_list_authenticated_only_views(self):
        """authenticated only views return 403 for guests"""
        for url in LISTS_URLS:
            self.access_all_categories()

            response = self.client.get('/' + url)
            self.assertEqual(response.status_code, 200)

            self.access_all_categories()

            response = self.client.get(self.category_b.get_absolute_url() + url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.category_b.name, response.content)

        self.logout_user()
        self.user = self.get_anonymous_user()
        for url in LISTS_URLS[1:]:
            self.access_all_categories()

            response = self.client.get('/' + url)
            self.assertEqual(response.status_code, 403)

            self.access_all_categories()
            response = self.client.get(self.category_b.get_absolute_url() + url)
            self.assertEqual(response.status_code, 403)

    def test_empty_list_hides_categories_picker(self):
        """categories picker is hidden on empty list"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(self.root, position='last-child', save=True)
        test_category = Category.objects.get(slug='hidden-category')

        self.access_all_categories()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(
            'subcategory-%s' % self.category_a.css_class, response.content)
        self.assertNotIn(
            'subcategory-%s' % self.category_e.css_class, response.content)

        self.access_all_categories()
        response = self.client.get(self.category_a.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(
            'subcategory-%s' % self.category_b.css_class, response.content)

    def test_list_renders_categories_picker(self):
        """categories picker renders valid categories"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(self.root, position='last-child', save=True)
        test_category = Category.objects.get(slug='hidden-category')

        testutils.post_thread(
            category=self.category_b,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'subcategory-%s' % self.category_a.css_class, response.content)

        # readable categories, but non-accessible directly
        self.assertNotIn(
            'subcategory-%s' % self.category_b.css_class, response.content)
        self.assertNotIn(
            'subcategory-%s' % self.category_c.css_class, response.content)
        self.assertNotIn(
            'subcategory-%s' % self.category_d.css_class, response.content)
        self.assertNotIn(
            'subcategory-%s' % self.category_f.css_class, response.content)

        # hidden category
        self.assertNotIn(
            'subcategory-%s' % test_category.css_class, response.content)

        # test category view
        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        self.assertIn(
            'subcategory-%s' % self.category_b.css_class, response.content)

        # readable categories, but non-accessible directly
        self.assertNotIn(
            'subcategory-%s' % self.category_c.css_class, response.content)
        self.assertNotIn(
            'subcategory-%s' % self.category_d.css_class, response.content)
        self.assertNotIn(
            'subcategory-%s' % self.category_f.css_class, response.content)


class CategoryThreadsListTests(ThreadsListTestCase):
    def test_access_hidden_category(self):
        """hidden category returns 404"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(self.root, position='last-child', save=True)
        test_category = Category.objects.get(slug='hidden-category')

        for url in LISTS_URLS:
            response = self.client.get(test_category.get_absolute_url() + url)
            self.assertEqual(response.status_code, 404)

    def test_access_protected_category(self):
        """protected category returns 403"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(self.root, position='last-child', save=True)
        test_category = Category.objects.get(slug='hidden-category')

        for url in LISTS_URLS:
            override_acl(self.user, {
                'visible_categories': [test_category.pk],
                'categories': {
                    test_category.pk: {
                        'can_see': 1,
                        'can_browse': 0,
                    }
                }
            });

            response = self.client.get(test_category.get_absolute_url() + url)
            self.assertEqual(response.status_code, 403)


class ThreadsVisibilityTests(ThreadsListTestCase):
    def test_list_renders_test_thread(self):
        """list renders test thread with valid top category"""
        test_thread = testutils.post_thread(
            category=self.category_c,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertIn(test_thread.get_absolute_url(), response.content)

        self.assertIn(
            'subcategory-%s' % self.category_a.css_class, response.content)
        self.assertIn(
            'thread-category-%s' % self.category_a.css_class, response.content)
        self.assertIn(
            'thread-category-%s' % self.category_c.css_class, response.content)

        # other top category is hidden from user
        self.assertNotIn(
            'subcategory-%s' % self.category_e.css_class, response.content)

        # test category view
        self.access_all_categories()
        response = self.client.get(self.category_b.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # thread displays
        self.assertIn(test_thread.get_absolute_url(), response.content)

        self.assertNotIn(
            'thread-category-%s' % self.category_b.css_class, response.content)
        self.assertIn(
            'thread-category-%s' % self.category_c.css_class, response.content)

        # category picker was update
        self.assertIn(
            'subcategory-%s' % self.category_c.css_class, response.content)
        self.assertNotIn(
            'subcategory-%s' % self.category_d.css_class, response.content)

    def test_list_renders_hidden_thread(self):
        """list renders empty due to no permission to see thread"""
        Category(
            name='Hidden Category',
            slug='hidden-category',
        ).insert_at(self.root, position='last-child', save=True)
        test_category = Category.objects.get(slug='hidden-category')

        test_thread = testutils.post_thread(
            category=test_category,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("empty-message", response.content)

    def test_list_user_see_own_moderated_thread(self):
        """list renders moderated thread that belongs to viewer"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
            is_moderated=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

    def test_list_user_cant_see_moderated_thread(self):
        """list hides moderated thread that belongs to other user"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_moderated=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_user_cant_see_hidden_thread(self):
        """list hides hidden thread that belongs to other user"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_hidden=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_user_cant_see_own_hidden_thread(self):
        """list hides hidden thread that belongs to viewer"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
            is_hidden=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_user_can_see_own_hidden_thread(self):
        """list shows hidden thread that belongs to viewer due to permission"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
            is_hidden=True,
        )

        self.access_all_categories({
            'can_hide_threads': 1
        })

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

    def test_list_user_can_see_hidden_thread(self):
        """
        list shows hidden thread that belongs to other user due to permission
        """
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_hidden=True,
        )

        self.access_all_categories({
            'can_hide_threads': 1
        })

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

    def test_list_user_can_see_moderated_thread(self):
        """
        list shows hidden thread that belongs to other user due to permission
        """
        test_thread = testutils.post_thread(
            category=self.category_a,
            is_moderated=True,
        )

        self.access_all_categories({
            'can_review_moderated_content': 1
        })

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)


class MyThreadsListTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """list renders empty"""
        self.access_all_categories()

        response = self.client.get('/my/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("empty-message", response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'my/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("empty-message", response.content)

    def test_list_renders_test_thread(self):
        """list renders only threads posted by user"""
        test_thread = testutils.post_thread(
            category=self.category_a,
            poster=self.user,
        )

        other_thread = testutils.post_thread(
            category=self.category_a,
        )

        self.access_all_categories()

        response = self.client.get('/my/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)
        self.assertNotIn(other_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'my/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)
        self.assertNotIn(other_thread.get_absolute_url(), response.content)


class NewThreadsListTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """list renders empty"""
        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("empty-message", response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("empty-message", response.content)

    def test_list_renders_new_thread(self):
        """list renders new thread"""
        test_thread = testutils.post_thread(
            category=self.category_a,
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

    def test_list_renders_thread_bumped_after_user_cutoff(self):
        """list renders new thread bumped after user cutoff"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=10)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.reads_cutoff - timedelta(days=2)
        )

        testutils.reply_thread(test_thread,
            posted_on=self.user.reads_cutoff + timedelta(days=4)
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_global_cutoff_thread(self):
        """list hides thread started before global cutoff"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=10)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=timezone.now() - timedelta(
                days=settings.MISAGO_FRESH_CONTENT_PERIOD + 1
            )
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_user_cutoff_thread(self):
        """list hides thread started before users cutoff"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=5)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.reads_cutoff - timedelta(minutes=1)
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_user_read_thread(self):
        """list hides thread already read by user"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=5)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(
            self.user, test_thread, test_thread.last_post)

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_category_read_thread(self):
        """list hides thread already read by user"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=5)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a
        )

        self.user.categoryread_set.create(
            category=self.category_a,
            last_read_on=timezone.now(),
        )

        self.access_all_categories()

        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(self.category_a.get_absolute_url() + 'new/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)


class UnreadThreadsListTests(ThreadsListTestCase):
    def test_list_renders_empty(self):
        """list renders empty"""
        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("empty-message", response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("empty-message", response.content)

    def test_list_renders_unread_thread(self):
        """list renders thread with unread posts"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=5)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(
            self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(test_thread)

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_never_read_thread(self):
        """list hides never read thread"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=5)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a
        )

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_read_thread(self):
        """list hides read thread"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=5)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(
            self.user, test_thread, test_thread.last_post)

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_global_cutoff_thread(self):
        """list hides thread replied before global cutoff"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=10)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=timezone.now() - timedelta(
                days=settings.MISAGO_FRESH_CONTENT_PERIOD + 5
            )
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(
            self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(test_thread,
            posted_on=test_thread.started_on + timedelta(days=1)
        )

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_user_cutoff_thread(self):
        """list hides thread replied before user cutoff"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=10)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.reads_cutoff - timedelta(days=2)
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(
            self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(test_thread,
            posted_on=test_thread.started_on + timedelta(days=1)
        )

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

    def test_list_hides_category_cutoff_thread(self):
        """list hides thread replied before category cutoff"""
        self.user.reads_cutoff = timezone.now() - timedelta(days=10)
        self.user.joined_on = self.user.reads_cutoff
        self.user.save()

        test_thread = testutils.post_thread(
            category=self.category_a,
            started_on=self.user.reads_cutoff - timedelta(days=2)
        )

        threadstracker.make_thread_read_aware(self.user, test_thread)
        threadstracker.read_thread(
            self.user, test_thread, test_thread.last_post)

        testutils.reply_thread(test_thread)

        self.user.categoryread_set.create(
            category=self.category_a,
            last_read_on=timezone.now(),
        )

        self.access_all_categories()

        response = self.client.get('/unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)

        self.access_all_categories()

        response = self.client.get(
            self.category_a.get_absolute_url() + 'unread/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_thread.get_absolute_url(), response.content)