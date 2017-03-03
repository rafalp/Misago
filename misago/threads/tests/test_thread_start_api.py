# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase


class StartThreadTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(StartThreadTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.api_link = reverse('misago:api:thread-list')

    def override_acl(self, extra_acl=None):
        new_acl = self.user.acl_cache
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 1,
            'can_pin_threads': 0,
            'can_close_threads': 0,
            'can_hide_threads': 0,
            'can_hide_own_threads': 0,
        })

        if extra_acl:
            new_acl['categories'][self.category.pk].update(extra_acl)

            if 'can_see' in extra_acl and not extra_acl['can_see']:
                new_acl['visible_categories'].remove(self.category.pk)
                new_acl['browseable_categories'].remove(self.category.pk)

            if 'can_browse' in extra_acl and not extra_acl['can_browse']:
                new_acl['browseable_categories'].remove(self.category.pk)

        override_acl(self.user, new_acl)

    def test_cant_start_thread_as_guest(self):
        """user has to be authenticated to be able to post thread"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_cant_see(self):
        """has no permission to see selected category"""
        self.override_acl({'can_see': 0})

        response = self.client.post(self.api_link, {
            'category': self.category.pk,
        })

        self.assertContains(response, "Selected category is invalid.", status_code=400)

    def test_cant_browse(self):
        """has no permission to browse selected category"""
        self.override_acl({'can_browse': 0})

        response = self.client.post(self.api_link, {
            'category': self.category.pk,
        })

        self.assertContains(response, "Selected category is invalid.", status_code=400)

    def test_cant_start_thread(self):
        """permission to start thread in category is validated"""
        self.override_acl({'can_start_threads': 0})

        response = self.client.post(self.api_link, {
            'category': self.category.pk,
        })

        self.assertContains(
            response, "You don't have permission to start new threads", status_code=400
        )

    def test_cant_start_thread_in_locked_category(self):
        """can't post in closed category"""
        self.category.is_closed = True
        self.category.save()

        self.override_acl({'can_close_threads': 0})

        response = self.client.post(self.api_link, {
            'category': self.category.pk,
        })

        self.assertContains(response, "This category is closed.", status_code=400)

    def test_cant_start_thread_in_invalid_category(self):
        """can't post in invalid category"""
        self.category.is_closed = True
        self.category.save()

        self.override_acl({'can_close_threads': 0})

        response = self.client.post(self.api_link, {'category': self.category.pk * 100000})

        self.assertContains(response, "Selected category doesn't exist", status_code=400)

    def test_empty_data(self):
        """no data sent handling has no showstoppers"""
        self.override_acl()

        response = self.client.post(self.api_link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'category': ["You have to select category to post thread in."],
                'title': ["You have to enter thread title."],
                'post': ["You have to enter a message."],
            }
        )

    def test_title_is_validated(self):
        """title is validated"""
        self.override_acl()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "------",
                'post': "Lorem ipsum dolor met, sit amet elit!",
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'title': ["Thread title should contain alpha-numeric characters."],
            }
        )

    def test_post_is_validated(self):
        """post is validated"""
        self.override_acl()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Lorem ipsum dolor met",
                'post': "a",
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'post': ["Posted message should be at least 5 characters long (it has 1)."],
            }
        )

    def test_can_start_thread(self):
        """endpoint creates new thread"""
        self.override_acl()
        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]

        response_json = response.json()
        self.assertEqual(response_json['url'], thread.get_absolute_url())

        self.override_acl()
        response = self.client.get(thread.get_absolute_url())
        self.assertContains(response, self.category.name)
        self.assertContains(response, thread.title)
        self.assertContains(response, "<p>Lorem ipsum dolor met!</p>")

        # api increased user's threads and posts counts
        self.reload_user()
        self.assertEqual(self.user.threads, 1)
        self.assertEqual(self.user.posts, 1)

        self.assertEqual(thread.category_id, self.category.pk)
        self.assertEqual(thread.title, "Hello, I am test thread!")
        self.assertEqual(thread.starter_id, self.user.id)
        self.assertEqual(thread.starter_name, self.user.username)
        self.assertEqual(thread.starter_slug, self.user.slug)
        self.assertEqual(thread.last_poster_id, self.user.id)
        self.assertEqual(thread.last_poster_name, self.user.username)
        self.assertEqual(thread.last_poster_slug, self.user.slug)

        post = self.user.post_set.all()[:1][0]
        self.assertEqual(post.category_id, self.category.pk)
        self.assertEqual(post.original, 'Lorem ipsum dolor met!')
        self.assertEqual(post.poster_id, self.user.id)
        self.assertEqual(post.poster_name, self.user.username)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.threads, 1)
        self.assertEqual(category.posts, 1)
        self.assertEqual(category.last_thread_id, thread.id)
        self.assertEqual(category.last_thread_title, thread.title)
        self.assertEqual(category.last_thread_slug, thread.slug)

        self.assertEqual(category.last_poster_id, self.user.id)
        self.assertEqual(category.last_poster_name, self.user.username)
        self.assertEqual(category.last_poster_slug, self.user.slug)

    def test_start_closed_thread_no_permission(self):
        """permission is checked before thread is closed"""
        self.override_acl({'can_close_threads': 0})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'close': True,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_closed)

    def test_start_closed_thread(self):
        """can post closed thread"""
        self.override_acl({'can_close_threads': 1})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'close': True,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_closed)

    def test_start_unpinned_thread(self):
        """can post unpinned thread"""
        self.override_acl({'can_pin_threads': 1})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'pin': 0,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 0)

    def test_start_locally_pinned_thread(self):
        """can post locally pinned thread"""
        self.override_acl({'can_pin_threads': 1})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'pin': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 1)

    def test_start_globally_pinned_thread(self):
        """can post globally pinned thread"""
        self.override_acl({'can_pin_threads': 2})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'pin': 2,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 2)

    def test_start_globally_pinned_thread_no_permission(self):
        """cant post globally pinned thread without permission"""
        self.override_acl({'can_pin_threads': 1})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'pin': 2,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 0)

    def test_start_locally_pinned_thread_no_permission(self):
        """cant post locally pinned thread without permission"""
        self.override_acl({'can_pin_threads': 0})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'pin': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertEqual(thread.weight, 0)

    def test_start_hidden_thread(self):
        """can post hidden thread"""
        self.override_acl({'can_hide_threads': 1})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'hide': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_hidden)

        category = Category.objects.get(pk=self.category.pk)
        self.assertNotEqual(category.last_thread_id, thread.id)

    def test_start_hidden_thread_no_permission(self):
        """cant post hidden thread without permission"""
        self.override_acl({'can_hide_threads': 0})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
                'hide': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_hidden)

    def test_post_unicode(self):
        """unicode characters can be posted"""
        self.override_acl()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Brzęczyżczykiewicz",
                'post': "Chrzążczyżewoszyce, powiat Łękółody.",
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_category_moderation_queue(self):
        """start unapproved thread in category that requires approval"""
        self.category.require_threads_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

        category = Category.objects.get(slug='first-category')
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts)
        self.assertFalse(category.last_thread_id == thread.id)

    def test_category_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        override_acl(self.user, {'can_approve_content': 1})

        self.category.require_threads_approval = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug='first-category')
        self.assertEqual(category.threads, self.category.threads + 1)
        self.assertEqual(category.posts, self.category.posts + 1)
        self.assertEqual(category.last_thread_id, thread.id)

    def test_user_moderation_queue(self):
        """start unapproved thread in category that requires approval"""
        self.override_acl({'require_threads_approval': 1})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertTrue(thread.is_unapproved)
        self.assertTrue(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_unapproved)

        category = Category.objects.get(slug='first-category')
        self.assertEqual(category.threads, self.category.threads)
        self.assertEqual(category.posts, self.category.posts)
        self.assertFalse(category.last_thread_id == thread.id)

    def test_user_moderation_queue_bypass(self):
        """bypass moderation queue due to user's acl"""
        override_acl(self.user, {'can_approve_content': 1})

        self.override_acl({'require_threads_approval': 1})

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug='first-category')
        self.assertEqual(category.threads, self.category.threads + 1)
        self.assertEqual(category.posts, self.category.posts + 1)
        self.assertEqual(category.last_thread_id, thread.id)

    def test_omit_other_moderation_queues(self):
        """other queues are omitted"""
        self.category.require_replies_approval = True
        self.category.require_edits_approval = True
        self.category.save()

        self.override_acl({
            'require_replies_approval': 1,
            'require_edits_approval': 1,
        })

        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': "Hello, I am test thread!",
                'post': "Lorem ipsum dolor met!",
            }
        )
        self.assertEqual(response.status_code, 200)

        thread = self.user.thread_set.all()[:1][0]
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_unapproved)

        category = Category.objects.get(slug='first-category')
        self.assertEqual(category.threads, self.category.threads + 1)
        self.assertEqual(category.posts, self.category.posts + 1)
        self.assertEqual(category.last_thread_id, thread.id)
