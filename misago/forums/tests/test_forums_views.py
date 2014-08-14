from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase

from misago.forums.lists import get_forums_list
from misago.forums.models import Forum


class ForumViewsTests(AdminTestCase):
    def test_index(self):
        """index contains forums list"""
        response = self.client.get(reverse('misago:index'))

        for node in get_forums_list(self.test_admin):
            self.assertIn(node.name, response.content)
            if node.level > 1:
                self.assertIn(node.get_absolute_url(), response.content)

    def test_index_no_perms(self):
        """index contains no visible forums"""
        override_acl(self.test_admin, {'visible_forums': []})
        response = self.client.get(reverse('misago:index'))

        for node in get_forums_list(self.test_admin):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotIn(node.get_absolute_url(), response.content)


class CategoryViewsTests(AdminTestCase):
    def setUp(self):
        super(CategoryViewsTests, self).setUp()
        categories_qs = Forum.objects.all_forums().filter(role='category')
        master_category = categories_qs[:1][0]

        self.category = Forum(role='category',
                              name='Test category',
                              slug='test-category')
        self.category.insert_at(master_category, save=True)

    def test_cant_see_category(self):
        """can't see category"""
        override_acl(self.test_admin, {'visible_forums': []})

        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_cant_browse_category(self):
        """can't see category"""
        override_acl(self.test_admin, {
            'visible_forums': [self.category.parent_id, self.category.pk],
            'forums': {
                self.category.parent_id: {'can_see': 1, 'can_browse': 1},
                self.category.pk: {'can_see': 1, 'can_browse': 0},
            }
        })

        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_can_browse_category(self):
        """can see category contents"""
        override_acl(self.test_admin, {
            'visible_forums': [self.category.parent_id, self.category.pk],
            'forums': {
                self.category.parent_id: {'can_see': 1, 'can_browse': 1},
                self.category.pk: {'can_see': 1, 'can_browse': 1},
            }
        })

        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class RedirectViewsTests(AdminTestCase):
    def setUp(self):
        super(RedirectViewsTests, self).setUp()
        redirects_qs = Forum.objects.all_forums().filter(role='redirect')
        self.redirect = redirects_qs[:1][0]

    def test_cant_see_redirect(self):
        """can't see redirect"""
        override_acl(self.test_admin, {'visible_forums': []})

        response = self.client.get(self.redirect.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_can_follow_redirect(self):
        """can see redirect"""
        override_acl(self.test_admin, {
            'visible_forums': [self.redirect.parent_id, self.redirect.pk],
            'forums': {
                self.redirect.parent_id: {'can_see': 1, 'can_browse': 1},
                self.redirect.pk: {'can_see': 1, 'can_browse': 1},
            }
        })

        response = self.client.get(self.redirect.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://misago-project.org')

        # Redirects count increased
        updated_redirect = Forum.objects.get(id=self.redirect.pk)
        self.assertEqual(updated_redirect.redirects_count,
                         self.redirect.redirects_count + 1)

        # Session keeps track of clicks spam
        self.client.get(self.redirect.get_absolute_url())
        self.client.get(self.redirect.get_absolute_url())
        self.client.get(self.redirect.get_absolute_url())
        self.client.get(self.redirect.get_absolute_url())

        updated_redirect = Forum.objects.get(id=self.redirect.pk)
        self.assertEqual(updated_redirect.redirects_count,
                         self.redirect.redirects_count + 1)
