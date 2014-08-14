from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.admin.testutils import AdminTestCase
from misago.core import threadstore
from misago.core.cache import cache

from misago.users.warnings import warn_user
from misago.users.models import WarningLevel


class WarningTestCase(AdminTestCase):
    def setUp(self):
        super(WarningTestCase, self).setUp()
        self.test_user = get_user_model().objects.create_user(
            "Bob", "bob@bob.com", "Pass.123")
        self.link_kwargs = {'user_slug': 'bob', 'user_id': self.test_user.pk}

        self.warning_levels = (
            WarningLevel.objects.create(name='Lvl 1'),
            WarningLevel.objects.create(name='Lvl 2'),
            WarningLevel.objects.create(name='Lvl 3'),
            WarningLevel.objects.create(name='Lvl 4'),
        )

        cache.clear()
        threadstore.clear()

    def warn_user(self, reason):
        override_acl(self.test_admin, {'can_warn_users': 1})
        response = self.client.post(
            reverse('misago:warn_user', kwargs=self.link_kwargs),
            data={'reason': reason})


class WarnUserTests(WarningTestCase):
    def test_no_permission(self):
        """fail to warn due to permissions"""
        override_acl(self.test_admin, {
            'can_warn_users': 0,
        })

        override_acl(self.test_user, {
            'can_be_warned': 1,
        })

        response = self.client.get(reverse('misago:warn_user',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 403)

    def test_protected_user(self):
        """fail to warn due to user's can_be_warned"""
        override_acl(self.test_admin, {
            'can_warn_users': 1,
        })

        override_acl(self.test_user, {
            'can_be_warned': 0,
        })

        response = self.client.get(reverse('misago:warn_user',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 403)

    def test_warn_user(self):
        """can warn user to the roof"""
        override_acl(self.test_admin, {
            'can_warn_users': 1,
        })

        override_acl(self.test_user, {
            'can_be_warned': 1,
        })

        for level in self.warning_levels:
            response = self.client.get(reverse('misago:warn_user',
                                               kwargs=self.link_kwargs))
            self.assertEqual(response.status_code, 200)

            response = self.client.post(
                reverse('misago:warn_user', kwargs=self.link_kwargs),
                data={'reason': 'Warning %s' % level.name})
            self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_user.warnings.count(), 4)


class UserWarningsListTests(WarningTestCase):
    def allow_warning(self):
        override_acl(self.test_admin, {
            'can_warn_users': 1,
            'can_see_other_users_warnings': 1,
        })

        override_acl(self.test_user, {
            'can_be_warned': 1,
        })

    def test_no_permission(self):
        """can't see other user warnings"""
        self.warn_user('Test Warning!')

        override_acl(self.test_admin, {
            'can_see_other_users_warnings': 0,
        })
        response = self.client.get(reverse('misago:user_warnings',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 404)

    def test_see_user_warnings(self):
        """can see user warnings"""
        self.allow_warning()
        response = self.client.get(reverse('misago:user_warnings',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob has no warnings', response.content)

        self.warn_user('Test Warning!')

        self.allow_warning()
        response = self.client.get(reverse('misago:user_warnings',
                                           kwargs=self.link_kwargs))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Warning!', response.content)


class CancelWarningTests(WarningTestCase):
    def allow_cancel_owned_warning(self):
        override_acl(self.test_admin, {
            'can_warn_users': 1,
            'can_see_other_users_warnings': 1,
            'can_cancel_warnings': 1,
        })

    def allow_cancel_all_warnings(self):
        override_acl(self.test_admin, {
            'can_warn_users': 1,
            'can_see_other_users_warnings': 1,
            'can_cancel_warnings': 2,
        })

    def test_no_permission(self):
        """can't cancel warnings"""
        override_acl(self.test_admin, {
            'can_warn_users': 1,
            'can_see_other_users_warnings': 1,
            'can_cancel_warnings': 0,
        })

        warning = warn_user(self.test_admin, self.test_user)
        response = self.client.post(
            reverse('misago:cancel_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.test_user.warnings.get(id=warning.pk).is_canceled)

    def test_no_permission_other(self):
        """can't cancel other mod warnings"""
        warning = warn_user(self.test_user, self.test_user)

        self.allow_cancel_owned_warning()
        response = self.client.post(
            reverse('misago:cancel_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.test_user.warnings.get(id=warning.pk).is_canceled)

        warning = warn_user(self.test_admin, self.test_user)
        self.allow_cancel_owned_warning()
        response = self.client.post(
            reverse('misago:cancel_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 302)

        warning = self.test_user.warnings.get(id=warning.pk)
        self.assertTrue(self.test_user.warnings.get(id=warning.pk).is_canceled)

    def test_cancel_other_and_owned_warnings(self):
        """cancel everyone's warnings"""
        warning = warn_user(self.test_user, self.test_user)

        self.allow_cancel_all_warnings()
        response = self.client.post(
            reverse('misago:cancel_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.test_user.warnings.get(id=warning.pk).is_canceled)

        warning = warn_user(self.test_admin, self.test_user)

        self.allow_cancel_all_warnings()
        response = self.client.post(
            reverse('misago:cancel_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.test_user.warnings.get(id=warning.pk).is_canceled)


class DeleteWarningTests(WarningTestCase):
    def allow_delete_owned_warning(self):
        override_acl(self.test_admin, {
            'can_warn_users': 1,
            'can_see_other_users_warnings': 1,
            'can_delete_warnings': 1,
        })

    def allow_delete_all_warnings(self):
        override_acl(self.test_admin, {
            'can_warn_users': 1,
            'can_see_other_users_warnings': 1,
            'can_delete_warnings': 2,
        })

    def test_no_permission(self):
        """can't delete warnings"""
        override_acl(self.test_admin, {
            'can_warn_users': 1,
            'can_see_other_users_warnings': 1,
            'can_delete_warnings': 0,
        })

        warning = warn_user(self.test_admin, self.test_user)
        response = self.client.post(
            reverse('misago:delete_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.test_user.warnings.count(), 1)

    def test_no_permission_other(self):
        """can't delete other mod warnings"""
        warning = warn_user(self.test_user, self.test_user)

        self.allow_delete_owned_warning()
        response = self.client.post(
            reverse('misago:delete_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.test_user.warnings.count(), 1)

        warning = warn_user(self.test_admin, self.test_user)

        self.allow_delete_owned_warning()
        response = self.client.post(
            reverse('misago:delete_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.test_user.warnings.count(), 1)

    def test_delete_other_and_owned_warnings(self):
        """delete everyone's warnings"""
        warning = warn_user(self.test_user, self.test_user)

        self.allow_delete_all_warnings()
        response = self.client.post(
            reverse('misago:delete_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.test_user.warnings.count(), 0)

        warning = warn_user(self.test_admin, self.test_user)

        self.allow_delete_all_warnings()
        response = self.client.post(
            reverse('misago:delete_warning', kwargs={
                'user_slug': 'bob',
                'user_id': self.test_user.pk,
                'warning_id': warning.pk
            }))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.test_user.warnings.count(), 0)
