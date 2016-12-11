from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.utils import formats
from django.utils.translation import ugettext as _
from django.test import override_settings
from rest_framework import status

from misago.admin.testutils import AdminTestCase


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class TestDjangoAdminUserForm(AdminTestCase):
    def setUp(self):
        super(TestDjangoAdminUserForm, self).setUp()
        self.test_user = get_user_model().objects.create_user(
            username='Bob',
            email='bob@test.com',
            password='Pass.123',
        )
        self.test_user_edit_view_url = reverse(
            viewname='admin:misago_users_user_change',
            args=[self.test_user.id],
        )

    def test_user_edit_view_content(self):
        """Basic data about a misago user could be viewed through django-admin."""
        user_edit_page = self.client.get(self.test_user_edit_view_url)
        
        self.assertEqual(user_edit_page.status_code, status.HTTP_200_OK)
        
        self.assertContains(user_edit_page, self.test_user.username)
        self.assertContains(user_edit_page, self.test_user.email)
        self.assertContains(user_edit_page, self.test_user.rank)
        
        last_login_date = formats.date_format(self.test_user.last_login)
        self.assertContains(user_edit_page, last_login_date)
        
        register_date = formats.date_format(self.test_user.joined_on)
        self.assertContains(user_edit_page, register_date)
        
        user_permissions = Permission.objects.all()
        for permission in user_permissions:
            self.assertContains(user_edit_page, permission)

    def test_user_edit_view_post(self):
        """A misago user permissions could be altered through django-admin."""
        perms_all = Permission.objects.all()
        perms_all_ids = []
        for perm in perms_all:
            perms_all_ids.append(perm.id)
        
        response = self.client.post(
            path=self.test_user_edit_view_url,
            data={'user_permissions': perms_all_ids},
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        user_perms_all = self.test_user.user_permissions.all()
        for perm_id in perms_all_ids:
            is_user_has_perm = user_perms_all.filter(id=perm_id).exists()
            self.assertTrue(is_user_has_perm)

    def test_misago_admin_url_presence_in_user_edit_view(self):
        """URL to misago admin is present in django-admin user edit view."""
        user_edit_page = self.client.get(self.test_user_edit_view_url)
        user_edit_from_misago_admin_url = reverse(
            viewname='misago:admin:users:accounts:edit',
            kwargs={'pk': self.test_user.pk},
        )
        self.assertContains(user_edit_page, user_edit_from_misago_admin_url)
        edit_from_misago_short_desc = _("Edit the user from Misago admin panel")
        self.assertContains(user_edit_page, edit_from_misago_short_desc)

    def test_misago_admin_url_presence_in_user_list_view(self):
        """URL to misago admin is present in django-admin user list view."""
        user_list_page = self.client.get(
            path=reverse('admin:misago_users_user_changelist'),
        )
        user_edit_from_misago_admin_url = reverse(
            viewname='misago:admin:users:accounts:edit',
            kwargs={'pk': self.test_user.pk},
        )
        self.assertContains(user_list_page, user_edit_from_misago_admin_url)
