from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class ForumIndexViewTests(TestCase):
    def test_forum_index_returns_200(self):
        """forum_index view has no show-stoppers"""
        c = Client()
        response = c.get(reverse('forum_index'))
        self.assertEqual(response.status_code, 200)
