# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.users.testutils import AuthenticatedUserTestCase


class PostMentionsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(PostMentionsTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.override_acl()

        self.post_link = reverse(
            'misago:api:thread-post-list', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

    def override_acl(self):
        new_acl = self.user.acl_cache
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 1,
            'can_reply_threads': 1,
        })

        override_acl(self.user, new_acl)

    def test_flood_has_no_showstoppers(self):
        """endpoint handles posting interruption"""
        response = self.client.post(
            self.post_link, data={
                'post': "This is test response!",
            }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.post_link, data={
                'post': "This is test response!",
            }
        )
        self.assertContains(
            response, "You can't post message so quickly after previous one.", status_code=403
        )
