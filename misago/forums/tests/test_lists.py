from django.test import TestCase

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase

from misago.forums.lists import get_forums_list, get_forum_path
from misago.forums.models import Forum


class GetForumListTests(AdminTestCase):
    def setUp(self):
        super(GetForumListTests, self).setUp()

        forums_acl = {'forums': {}, 'visible_forums': []}
        for forum in Forum.objects.all_forums():
            forums_acl['visible_forums'].append(forum.pk)
            forums_acl['forums'][forum.pk] = {'can_see': 1, 'can_browse': 1}
        override_acl(self.test_admin, forums_acl)

    def test_root_forums_list_no_parent(self):
        """get_forums_list returns all children of root nodes"""
        self.assertEqual(len(get_forums_list(self.test_admin)), 3)

    def test_root_forums_list_with_parents(self):
        """get_forums_list returns all children of given node"""
        for i, node in enumerate(get_forums_list(self.test_admin)):
            child_nodes = len(get_forums_list(self.test_admin, node))
            self.assertEqual(child_nodes, len(node.get_descendants()))


class GetForumPathTests(TestCase):
    def get_forum_path(self):
        """get_forums_list returns all children of root nodes"""
        for node in get_forums_list(self.test_admin):
            parent_nodes = len(get_forum_path(self.test_admin, node))
            self.assertEqual(parent_nodes, node.level - 1)
