from django.contrib.auth.models import Permission
from django.test import override_settings
from django.urls import reverse
from django.utils import formats

from ....admin.test import AdminTestCase
from ...test import create_test_user
from ..djangoadmin import UserAdminModel


@override_settings(ROOT_URLCONF="misago.core.testproject.urls")
class TestDjangoAdminUserForm(AdminTestCase):
    def setUp(self):
        super().setUp()
        self.test_user = create_test_user("OtherUser", "otheruser@example.com")
        self.edit_test_user_in_django_url = reverse(
            "admin:misago_users_user_change", args=[self.test_user.pk]
        )
        self.edit_test_user_in_misago_url = reverse(
            "misago:admin:users:edit", args=[self.test_user.pk]
        )

    def test_user_edit_view_content(self):
        """basic data about a user is present in Django admin"""
        response = self.client.get(self.edit_test_user_in_django_url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.test_user.username)
        self.assertContains(response, self.test_user.email)
        self.assertContains(response, self.test_user.rank)

        last_login_date = formats.date_format(self.test_user.last_login)
        self.assertContains(response, last_login_date)

        register_date = formats.date_format(self.test_user.joined_on)
        self.assertContains(response, register_date)

        user_permissions = Permission.objects.all()
        for permission in user_permissions:
            self.assertContains(response, permission)

    def test_user_edit_view_post(self):
        """user permissions are editable through Django admin"""
        perms_all = Permission.objects.all()
        perms_all_pks = []
        for perm in perms_all:
            perms_all_pks.append(perm.pk)

        response = self.client.post(
            self.edit_test_user_in_django_url, data={"user_permissions": perms_all_pks}
        )
        self.assertEqual(response.status_code, 302)

        user_perms = self.test_user.user_permissions.all()
        for perm_pk in perms_all_pks:
            is_user_has_perm = user_perms.filter(pk=perm_pk).exists()
            self.assertTrue(is_user_has_perm)

    def test_misago_admin_url_presence_in_user_edit_view(self):
        """the url to Misago admin is present in Django admin user edit view"""
        response = self.client.get(self.edit_test_user_in_django_url)
        self.assertContains(response, self.edit_test_user_in_misago_url)
        edit_from_misago_short_desc = (
            UserAdminModel.get_edit_from_misago_url.short_description
        )
        self.assertContains(response, edit_from_misago_short_desc)

    def test_misago_admin_url_presence_in_user_list_view(self):
        """the url to Misago admin is present in Django admin user list view"""
        response = self.client.get(reverse("admin:misago_users_user_changelist"))
        self.assertContains(response, self.edit_test_user_in_misago_url)
