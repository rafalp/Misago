from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase
from misago.forums.models import Forum


class ForumThreadsTests(AdminTestCase):
    def setUp(self):
        super(ForumThreadsTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.link = self.forum.get_absolute_url()

    def test_cant_see(self):
        """has no permission to see forum"""
        forums_acl = self.test_admin.acl
        forums_acl['visible_forums'].remove(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 0,
            'can_browse': 0,
        }
        override_acl(self.test_admin, forums_acl)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 404)

    def test_cant_browse(self):
        """has no permission to browse forum"""
        forums_acl = self.test_admin.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 1,
            'can_browse': 0,
        }
        override_acl(self.test_admin, forums_acl)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)

    def test_can_browse_empty(self):
        """has permission to browse forum, sees empty list"""
        forums_acl = self.test_admin.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = {
            'can_see': 1,
            'can_browse': 1,
        }
        override_acl(self.test_admin, forums_acl)

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No threads", response.content)
