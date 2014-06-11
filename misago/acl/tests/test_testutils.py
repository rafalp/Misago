from django.test import TestCase
from misago.acl.models import Role, ForumRole
from misago.acl.testutils import fake_post_data


class FakeTestDataTests(TestCase):
    def test_fake_post_data_for_role(self):
        """fake data was created for Role"""
        test_data = fake_post_data(Role(), {'can_fly': 1})

        self.assertIn('can_fly', test_data)

    def test_fake_post_data_for_forumrole(self):
        """fake data was created for ForumRole"""
        test_data = fake_post_data(ForumRole(), {'can_swim': 1})

        self.assertIn('can_swim', test_data)
