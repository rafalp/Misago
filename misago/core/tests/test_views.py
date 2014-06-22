from django.core.urlresolvers import reverse
from django.test import TestCase


class ForumIndexViewTests(TestCase):
    serialized_rollback = True

    def test_forum_index_returns_200(self):
        """forum_index view has no show-stoppers"""
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
