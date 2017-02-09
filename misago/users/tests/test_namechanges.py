from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users.namechanges import UsernameChanges


UserModel = get_user_model()


class UsernameChangesTests(TestCase):
    def test_username_changes_helper(self):
        """username changes are tracked correctly"""
        test_user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        namechanges = UsernameChanges(test_user)
        self.assertEqual(namechanges.left, 2)
        self.assertIsNone(namechanges.next_on)

        self.assertEqual(test_user.namechanges.count(), 0)

        test_user.set_username('Boberson')
        test_user.save(update_fields=['username', 'slug'])

        namechanges = UsernameChanges(test_user)
        self.assertEqual(namechanges.left, 1)
        self.assertIsNone(namechanges.next_on)

        self.assertEqual(test_user.namechanges.count(), 1)
