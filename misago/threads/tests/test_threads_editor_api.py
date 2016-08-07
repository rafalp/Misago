import json

from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadsApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.api_link = reverse('misago:api:thread-editor')

    def override_acl(self, acl=None):
        final_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_start_threads': 0,
            'can_reply_threads': 0,
            'can_edit_threads': 0,
            'can_edit_posts': 0,
            'can_hide_own_threads': 0,
            'can_hide_own_posts': 0,
            'thread_edit_time': 0,
            'post_edit_time': 0,
            'can_hide_threads': 0,
            'can_hide_posts': 0,
            'can_protect_posts': 0,
            'can_move_posts': 0,
            'can_merge_posts': 0,
            'can_pin_threads': 0,
            'can_close_threads': 0,
            'can_move_threads': 0,
            'can_merge_threads': 0,
            'can_split_threads': 0,
            'can_approve_content': 0,
            'can_report_content': 0,
            'can_see_reports': 0,
            'can_see_posts_likes': 0,
            'can_like_posts': 0,
            'can_hide_events': 0,
        }

        if acl:
            final_acl.update(acl)

        browseable_categories = []
        if final_acl['can_browse']:
            browseable_categories.append(self.category.pk)

        override_acl(self.user, {
            'browseable_categories': browseable_categories,
            'categories': {
                self.category.pk: final_acl
            }
        })

    def get_json(self):
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        return json.loads(smart_str(response.content))

    def test_anonymous_user_request(self):
        """endpoint validates if user is authenticated"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json['detail'], "You need to be signed in to post content.")

    def test_category_visibility_validation(self):
        """endpoint omits non-browseable categories"""
        self.override_acl({'can_browse': 0})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(len(response_json), 0)

    def test_category_disallowing_new_threads(self):
        """endpoint omits category disallowing starting threads"""
        self.override_acl({
            'can_start_threads': 0,
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(len(response_json), 0)

    def test_category_closed_disallowing_new_threads(self):
        """endpoint omits closed category"""
        self.override_acl({
            'can_start_threads': 2,
            'can_close_threads': 0,
        })

        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(len(response_json), 0)

    def test_category_closed_allowing_new_threads(self):
        """endpoint adds closed category that allows new threads"""
        self.override_acl({
            'can_start_threads': 2,
            'can_close_threads': 1,
        })

        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json[0], {
            'id': self.category.pk,
            'name': self.category.name,
            'level': 0,
            'post': {
                'close': True,
                'hide': False,
                'pin': 0
            }
        })

    def test_category_allowing_new_threads(self):
        """endpoint adds category that allows new threads"""
        self.override_acl({
            'can_start_threads': 2,
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json[0], {
            'id': self.category.pk,
            'name': self.category.name,
            'level': 0,
            'post': {
                'close': False,
                'hide': False,
                'pin': 0
            }
        })

    def test_category_allowing_closing_threads(self):
        """endpoint adds category that allows new closed threads"""
        self.override_acl({
            'can_start_threads': 2,
            'can_close_threads': 1,
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json[0], {
            'id': self.category.pk,
            'name': self.category.name,
            'level': 0,
            'post': {
                'close': True,
                'hide': False,
                'pin': 0
            }
        })

    def test_category_allowing_locally_pinned_threads(self):
        """endpoint adds category that allows locally pinned threads"""
        self.override_acl({
            'can_start_threads': 2,
            'can_pin_threads': 1,
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json[0], {
            'id': self.category.pk,
            'name': self.category.name,
            'level': 0,
            'post': {
                'close': False,
                'hide': False,
                'pin': 1
            }
        })

    def test_category_allowing_globally_pinned_threads(self):
        """endpoint adds category that allows globally pinned threads"""
        self.override_acl({
            'can_start_threads': 2,
            'can_pin_threads': 2,
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json[0], {
            'id': self.category.pk,
            'name': self.category.name,
            'level': 0,
            'post': {
                'close': False,
                'hide': False,
                'pin': 2
            }
        })

    def test_category_allowing_hidden_threads(self):
        """endpoint adds category that allows globally pinned threads"""
        self.override_acl({
            'can_start_threads': 2,
            'can_hide_threads': 1,
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json[0], {
            'id': self.category.pk,
            'name': self.category.name,
            'level': 0,
            'post': {
                'close': 0,
                'hide': 1,
                'pin': 0
            }
        })

        self.override_acl({
            'can_start_threads': 2,
            'can_hide_threads': 2,
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(smart_str(response.content))
        self.assertEqual(response_json[0], {
            'id': self.category.pk,
            'name': self.category.name,
            'level': 0,
            'post': {
                'close': False,
                'hide': True,
                'pin': 0
            }
        })
