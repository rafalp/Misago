from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase


class ChangeForumOptionsTests(AdminTestCase):
    def setUp(self):
        super(ChangeForumOptionsTests, self).setUp()
        self.view_link = reverse('misago:usercp_change_forum_options')

    def test_change_forum_options_get(self):
        """GET to usercp change options view returns 200"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Change forum options', response.content)

    def test_change_forum_options_post(self):
        """POST to usercp change options view returns 200"""
        response = self.client.post(self.view_link, data={
            'timezone': 'Asia/Qatar',
            'presence_visibility': '2',
            'subscribe_to_started_threads': '0',
            'subscribe_to_replied_threads': '1',
            })

        self.assertEqual(response.status_code, 302)

        test_user = get_user_model().objects.get(pk=self.test_admin.pk)
        self.assertEqual(test_user.timezone, 'Asia/Qatar')
        self.assertEqual(test_user.presence_visibility, 2)
        self.assertEqual(test_user.subscribe_to_started_threads, 0)
        self.assertEqual(test_user.subscribe_to_replied_threads, 1)
