from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Thread, Post
from misago.threads.testutils import post_thread, reply_thread


class PostViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(PostViewTestCase, self).setUp()

        self.category = Category.objects.all_categories().filter(role='forum')[:1][0]
        self.category.labels = []

        self.thread = post_thread(self.category)

    def override_acl(self, new_acl, category=None):
        new_acl.update({
            'can_see': True,
            'can_browse': True,
            'can_see_all_threads': True,
            'can_see_own_threads': False
        })

        category = category or self.category

        categories_acl = self.user.acl
        categories_acl['visible_categories'].append(category.pk)
        categories_acl['categories'][category.pk] = new_acl
        override_acl(self.user, categories_acl)


class ApprovePostViewTests(PostViewTestCase):
    def test_approve_thread(self):
        """view approves thread"""
        self.thread.first_post.is_moderated = True
        self.thread.first_post.save()

        self.thread.synchronize()
        self.thread.save()

        post_link = reverse('misago:approve_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_review_moderated_content': 1})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertFalse(thread.is_moderated)
        self.assertFalse(thread.has_moderated_posts)

    def test_approve_post(self):
        """view approves post"""
        post = reply_thread(self.thread, is_moderated=True)

        post_link = reverse('misago:approve_post', kwargs={
            'post_id': post.id
        })

        self.override_acl({'can_review_moderated_content': 1})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertFalse(thread.has_moderated_posts)


class UnhidePostViewTests(PostViewTestCase):
    def test_unhide_first_post(self):
        """attempt to reveal first post in thread fails"""
        post_link = reverse('misago:unhide_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_unhide_post_no_permission(self):
        """view fails due to lack of permissions"""
        post = reply_thread(self.thread, is_hidden=True)
        post_link = reverse('misago:unhide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 0, 'can_hide_own_posts': 0})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_unhide_post(self):
        """view reveals post"""
        post = reply_thread(self.thread, is_hidden=True)
        post_link = reverse('misago:unhide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        post = Post.objects.get(id=post.id)
        self.assertFalse(post.is_hidden)


class HidePostViewTests(PostViewTestCase):
    def test_hide_first_post(self):
        """attempt to hide first post in thread fails"""
        post_link = reverse('misago:hide_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_hide_post_no_permission(self):
        """view fails due to lack of permissions"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:hide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 0, 'can_hide_own_posts': 0})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_hide_post(self):
        """view hides post"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:hide_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        post = Post.objects.get(id=post.id)
        self.assertTrue(post.is_hidden)


class DeletePostViewTests(PostViewTestCase):
    def test_delete_first_post(self):
        """attempt to delete first post in thread fails"""
        post_link = reverse('misago:delete_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_delete_post_no_permission(self):
        """view fails due to lack of permissions"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:delete_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 0, 'can_hide_own_posts': 0})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 403)

    def test_delete_post(self):
        """view deletes post"""
        post = reply_thread(self.thread)
        post_link = reverse('misago:delete_post', kwargs={'post_id': post.id})

        self.override_acl({'can_hide_posts': 2})
        response = self.client.post(post_link)
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(thread.first_post_id, thread.last_post_id)
        self.assertEqual(thread.replies, 0)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)


class ReportPostViewTests(PostViewTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_cant_report_post(self):
        """can't access to report post view"""
        post_link = reverse('misago:report_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_report_content': 0})
        response = self.client.get(post_link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_report_post_get_form(self):
        """fetch report post form"""
        post_link = reverse('misago:report_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_report_content': 1})
        response = self.client.get(post_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Report post", response.content)

    def test_report_post_post_form(self):
        """post report post form"""
        post_link = reverse('misago:report_post', kwargs={
            'post_id': self.thread.first_post_id
        })

        self.override_acl({'can_report_content': 1})
        response = self.client.post(post_link, data={
            'message': 'Lorem ipsum dolor met!',
        }, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        # attempt reporting post again
        self.override_acl({'can_report_content': 1})
        response = self.client.get(post_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("already reported this post", response.content)
