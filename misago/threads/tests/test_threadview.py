from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.models import Thread
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadViewTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)

    def override_acl(self, acl=None):
        final_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
            'can_edit_posts': 0,
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
        }

        if acl:
            final_acl.update(acl)

        override_acl(self.user, {
            'categories': {
                self.category.pk: final_acl
            }
        })


class ThreadVisibilityTests(ThreadViewTestCase):
    def test_thread_displays(self):
        """thread view has no showstoppers"""
        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_shows_owner_thread(self):
        """view handles "owned threads only"""
        self.override_acl({
            'can_see_all_threads': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.thread.starter = self.user
        self.thread.save()

        self.override_acl({
            'can_see_all_threads': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_validates_category_permissions(self):
        """view validates category visiblity"""
        self.override_acl({
            'can_see': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.override_acl({
            'can_browse': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)
