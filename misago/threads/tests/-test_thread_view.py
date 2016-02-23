from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Thread, Label
from misago.threads.testutils import post_thread, reply_thread


class ThreadViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadViewTestCase, self).setUp()

        self.category = Category.objects.all_categories().filter(role='forum')[:1][0]
        self.category.labels = []

        self.thread = post_thread(self.category)

    def override_acl(self, new_acl, category=None):
        category = category or self.category

        new_acl.update({'can_see': True, 'can_browse': True})

        categories_acl = self.user.acl
        categories_acl['visible_categories'].append(category.pk)
        categories_acl['categories'][category.pk] = new_acl
        override_acl(self.user, categories_acl)

    def reload_thread(self):
        self.thread = Thread.objects.get(id=self.thread.id)
        return self.thread


class ThreadViewTests(ThreadViewTestCase):
    def test_can_see_all_threads_false(self):
        """its impossible to see thread made by other user"""
        self.override_acl({
            'can_see_all_threads': False,
            'can_see_own_threads': True
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_can_see_all_threads_false_owned_thread(self):
        """user can see thread he started in private category"""
        self.override_acl({
            'can_see_all_threads': False,
            'can_see_own_threads': True
        })

        self.thread.starter = self.user
        self.thread.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.thread.title, response.content)

    def test_can_see_all_threads_true(self):
        """its possible to see thread made by other user"""
        self.override_acl({
            'can_see_all_threads': True,
            'can_see_own_threads': False
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.thread.title, response.content)


class ThreadViewModerationTests(ThreadViewTestCase):
    def setUp(self):
        super(ThreadViewModerationTests, self).setUp()
        Label.objects.clear_cache()

    def tearDown(self):
        super(ThreadViewModerationTests, self).tearDown()
        Label.objects.clear_cache()

    def override_acl(self, new_acl, category=None):
        new_acl.update({
            'can_see_all_threads': True,
            'can_see_own_threads': False
        })
        super(ThreadViewModerationTests, self).override_acl(new_acl, category)

    def test_label_thread(self):
        """its possible to set thread label"""
        self.override_acl({'can_change_threads_labels': 0})
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Thread actions", response.content)

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Thread actions", response.content)

        test_label = Label.objects.create(name="Foxtrot", slug="foxtrot")
        test_label.categories.add(self.category)
        Label.objects.clear_cache()

        self.override_acl({'can_change_threads_labels': 0})
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Thread actions", response.content)

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_label.name, response.content)
        self.assertIn(test_label.slug, response.content)

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.post(self.thread.get_absolute_url(), data={
            'thread_action': 'label:%s' % test_label.slug
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.reload_thread().label_id, test_label.id)

    def test_change_thread_label(self):
        """its possible to change thread label"""
        test_label = Label.objects.create(name="Foxtrot", slug="foxtrot")
        test_label.categories.add(self.category)
        other_label = Label.objects.create(name="Uniform", slug="uniform")
        other_label.categories.add(self.category)

        Label.objects.clear_cache()

        self.thread.label = test_label
        self.thread.save()

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(test_label.name, response.content)
        self.assertNotIn(test_label.slug, response.content)
        self.assertIn(other_label.name, response.content)
        self.assertIn(other_label.slug, response.content)

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.post(self.thread.get_absolute_url(), data={
            'thread_action': 'label:%s' % test_label.slug
        })
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.post(self.thread.get_absolute_url(), data={
            'thread_action': 'label:%s' % other_label.slug
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.reload_thread().label_id, other_label.id)

    def test_unlabel_thread(self):
        """its possible to unset thread label"""
        test_label = Label.objects.create(name="Foxtrot", slug="foxtrot")
        test_label.categories.add(self.category)
        Label.objects.clear_cache()

        self.thread.label = test_label
        self.thread.save()

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('unlabel', response.content)

        self.override_acl({'can_change_threads_labels': 2})
        response = self.client.post(self.thread.get_absolute_url(), data={
            'thread_action': 'unlabel'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.reload_thread().label)

    def test_pin_thread(self):
        """its possible to pin thread"""
        self.override_acl({'can_pin_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'pin'})
        self.assertEqual(response.status_code, 200)

        # allow for pinning threads
        self.override_acl({'can_pin_threads': 1})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'pin'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.reload_thread().is_pinned)

    def test_unpin_thread(self):
        """its possible to unpin thread"""
        self.thread.is_pinned = True
        self.thread.save()

        self.override_acl({'can_pin_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'unpin'})
        self.assertEqual(response.status_code, 200)

        # allow for pinning threads
        self.override_acl({'can_pin_threads': 1})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'unpin'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.reload_thread().is_pinned)

    def test_approve_thread(self):
        """its possible to approve moderated thread"""
        self.thread.first_post.poster = self.user
        self.thread.first_post.poster_name = self.user.username
        self.thread.first_post.is_moderated = True
        self.thread.first_post.save()

        self.thread.synchronize()
        self.thread.save()

        self.override_acl({'can_review_moderated_content': 1})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'approve'})
        self.assertEqual(response.status_code, 302)

        self.assertFalse(self.reload_thread().is_moderated)
        self.assertFalse(self.reload_thread().first_post.is_moderated)

        self.override_acl({'can_review_moderated_content': 1})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'approve'})
        self.assertEqual(response.status_code, 200)

    def test_close_thread(self):
        """its possible to close thread"""
        self.override_acl({'can_close_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'close'})
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_close_threads': 2})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'close'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.reload_thread().is_closed)

    def test_open_thread(self):
        """its possible to close thread"""
        self.thread.is_closed = True
        self.thread.save()

        self.override_acl({'can_close_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'open'})
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_close_threads': 2})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'open'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.reload_thread().is_closed)

    def test_move_thread(self):
        """its possible to move thread"""
        self.override_acl({'can_move_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'move'})
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_move_threads': 1})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'move'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Move thread to category:", response.content)

        new_category = Category(
            name="New Category",
            slug="new-category",
            role='forum'
        )
        new_category.insert_at(self.category.parent, save=True)

        self.override_acl({'can_move_threads': 1})
        self.override_acl({'can_move_threads': 1}, new_category)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'thread_action': 'move',
            'new_category': unicode(new_category.id),
            'submit': '1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.reload_thread().category, new_category)

        # we made category "empty", assert that board index renders
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)

    def test_hide_thread(self):
        """its possible to hide thread"""
        self.override_acl({'can_hide_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'hide'})
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_hide_threads': 2})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'hide'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.reload_thread().is_hidden)

        # we made category "empty", assert that board index renders
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)

    def test_unhide_thread(self):
        """its possible to unhide thread"""
        self.override_acl({'can_hide_threads': 2})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'hide'})
        self.assertEqual(response.status_code, 302)

        self.override_acl({'can_hide_threads': 2})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'unhide'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.reload_thread().is_hidden)

    def test_delete_thread(self):
        """its possible to delete thread"""
        self.override_acl({'can_hide_threads': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'delete'})
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_hide_threads': 2})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'delete'})
        self.assertEqual(response.status_code, 302)

        # we made category empty, assert that board index renders
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)

    def test_approve_posts(self):
        """moderation allows for approving multiple posts"""
        posts = []
        for p in xrange(4):
            posts.append(reply_thread(self.thread, is_moderated=True))
        for p in xrange(4):
            posts.append(reply_thread(self.thread))

        self.assertTrue(self.reload_thread().has_moderated_posts)
        self.assertEqual(self.thread.replies, 4)

        test_acl = {
            'can_review_moderated_content': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Approve posts", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'approve', 'item': [p.pk for p in posts]
        })
        self.assertEqual(response.status_code, 302)

        self.assertFalse(self.reload_thread().has_moderated_posts)
        self.assertEqual(self.reload_thread().replies, 8)

        for post in posts:
            self.assertFalse(self.thread.post_set.get(id=post.id).is_moderated)

    def test_merge_posts(self):
        """moderation allows for merging multiple posts into one"""
        posts = []
        for p in xrange(4):
            posts.append(reply_thread(self.thread, poster=self.user))
        for p in xrange(4):
            posts.append(reply_thread(self.thread))

        self.thread.synchronize()
        self.assertEqual(self.thread.replies, 8)

        test_acl = {
            'can_merge_posts': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Merge posts into one", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'merge', 'item': [p.pk for p in posts[:1]]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("select at least two posts", response.content)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 8)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'merge', 'item': [p.pk for p in posts[3:5]]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("merge posts made by different authors",
                      response.content)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 8)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'merge', 'item': [p.pk for p in posts[5:7]]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("merge posts made by different authors",
                      response.content)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 8)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'merge', 'item': [p.pk for p in posts[:4]]
        })
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 5)

    def test_move_posts(self):
        """moderation allows for moving posts to other thread"""
        test_acl = {
            'can_move_posts': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Move posts", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'move', 'item': [self.thread.first_post_id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("first post", response.content)

        posts = [reply_thread(self.thread) for t in xrange(4)]

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'move',
            'item': [p.pk for p in posts],
            'new_thread_url': '',
            'submit': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('enter valid link to thread', response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'move',
            'item': [p.pk for p in posts],
            'new_thread_url': self.category.get_absolute_url(),
            'submit': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('enter valid link to thread', response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'move',
            'item': [p.pk for p in posts],
            'new_thread_url': self.thread.get_absolute_url(),
            'submit': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('thread is same as current one', response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'move',
            'item': [p.pk for p in posts]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Move posts', response.content)

        other_thread = post_thread(self.category)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'move',
            'item': [p.pk for p in posts[:3]],
            'new_thread_url': other_thread.get_absolute_url(),
            'submit': ''
        })
        self.assertEqual(response.status_code, 302)

        other_thread = Thread.objects.get(id=other_thread.id)
        self.assertEqual(other_thread.replies, 3)

        for post in posts[:3]:
            other_thread.post_set.get(id=post.id)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'move',
            'item': [posts[-1].pk],
            'new_thread_url': other_thread.get_absolute_url(),
            'follow': ''
        })
        self.assertEqual(response.status_code, 302)

    def test_split_thread(self):
        """moderation allows for splitting posts into new thread"""
        test_acl = {
            'can_split_threads': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Split posts", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'split', 'item': [self.thread.first_post_id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("first post", response.content)

        posts = [reply_thread(self.thread) for t in xrange(4)]

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'split',
            'item': [p.pk for p in posts]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Split thread', response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'split',
            'item': [p.pk for p in posts[:3]],
            'category': self.category.id,
            'thread_title': 'Split thread',
            'submit': ''
        })
        self.assertEqual(response.status_code, 302)

        new_thread = Thread.objects.get(slug='split-thread')
        self.assertEqual(new_thread.replies, 2)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'split',
            'item': [posts[-1].pk],
            'category': self.category.id,
            'thread_title': 'Split thread',
            'follow': ''
        })
        self.assertEqual(response.status_code, 302)

    def test_protect_unprotect_posts(self):
        """moderation allows for protecting and unprotecting multiple posts"""
        posts = [reply_thread(self.thread) for t in xrange(4)]

        self.thread.synchronize()
        self.assertEqual(self.thread.replies, 4)

        test_acl = {
            'can_protect_posts': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Protect posts", response.content)
        self.assertIn("Release posts", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'protect', 'item': [p.pk for p in posts[:2]]
        })
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 4)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'protect', 'item': [p.pk for p in posts[:2]]
        })
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 4)

        posts_queryset = self.thread.post_set
        for post in posts_queryset.filter(id__in=[p.pk for p in posts[:2]]):
            self.assertTrue(post.is_protected)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('This post is protected', response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'unprotect', 'item': [p.pk for p in posts[:2]]
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('This post is protected', response.content)

        for post in posts_queryset.filter(id__in=[p.pk for p in posts[:2]]):
            self.assertFalse(post.is_protected)

    def test_cant_delete_hide_unhide_first_post(self):
        """op is not deletable/hideable/unhideable"""
        test_acl = {
            'can_hide_posts': 2
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Delete posts", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'delete', 'item': [self.thread.first_post_id]
        })
        self.assertEqual(response.status_code, 200)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'hide', 'item': [self.thread.first_post_id]
        })
        self.assertEqual(response.status_code, 200)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'unhide', 'item': [self.thread.first_post_id]
        })
        self.assertEqual(response.status_code, 200)

    def test_hide_unhide_posts(self):
        """moderation allows for hiding and unhiding multiple posts"""
        posts = [reply_thread(self.thread) for t in xrange(4)]

        self.thread.synchronize()
        self.assertEqual(self.thread.replies, 4)

        test_acl = {
            'can_hide_posts': 1
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hide posts", response.content)
        self.assertIn("Reveal posts", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'hide', 'item': [p.pk for p in posts[:2]]
        })
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 4)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'hide', 'item': [p.pk for p in posts[:2]]
        })
        self.assertEqual(response.status_code, 302)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 4)

        posts_queryset = self.thread.post_set
        for post in posts_queryset.filter(id__in=[p.pk for p in posts[:2]]):
            self.assertTrue(post.is_hidden)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'unhide', 'item': [p.pk for p in posts[:2]]
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('hidden-message', response.content)

        for post in posts_queryset.filter(id__in=[p.pk for p in posts[:2]]):
            self.assertFalse(post.is_hidden)

    def test_delete_posts(self):
        """moderation allows for deleting posts"""
        posts = [reply_thread(self.thread) for t in xrange(10)]

        self.thread.synchronize()
        self.assertEqual(self.thread.replies, 10)

        test_acl = {
            'can_hide_posts': 2
        }

        self.override_acl(test_acl)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn("Delete posts", response.content)

        self.override_acl(test_acl)
        response = self.client.post(self.thread.get_absolute_url(), data={
            'action': 'delete', 'item': [p.pk for p in posts]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['location'].endswith(self.thread.get_absolute_url()))

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 0)

        posts = [reply_thread(self.thread) for t in xrange(30)]

        second_page_link = reverse('misago:thread', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug,
            'page': 2
        })

        self.override_acl(test_acl)
        response = self.client.post(second_page_link, data={
            'action': 'delete', 'item': [p.pk for p in posts[10:20]]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(second_page_link))

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 20)

        self.override_acl(test_acl)
        response = self.client.post(second_page_link, data={
            'action': 'delete', 'item': [p.pk for p in posts[:-10]]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['location'].endswith(self.thread.get_absolute_url()))

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertEqual(thread.replies, 10)
