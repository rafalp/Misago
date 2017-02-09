from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import override_settings
from django.urls import reverse
from django.utils import formats

from misago.admin.testutils import AdminTestCase


UserModel = get_user_model()


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class TestDjangoAdminUserForm(AdminTestCase):
    def test_edit_page_content(self):
        """assert that edit-view of `test_user` contains expected content."""
        test_user = UserModel.objects.create_user(
            username='Bob',
            email='bob@test.com',
            password='Pass.123',
        )

        test_user_edit_view = reverse(
            viewname='admin:misago_users_user_change',
            args=[test_user.id],
        )
        response = self.client.get(test_user_edit_view)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, test_user.username)
        self.assertContains(response, test_user.email)
        self.assertContains(response, test_user.rank)

        last_login_date = formats.date_format(test_user.last_login)
        register_date = formats.date_format(test_user.joined_on)
        self.assertContains(response, last_login_date)
        self.assertContains(response, register_date)

        edit_from_misago_admin_link = reverse(
            viewname='misago:admin:users:accounts:edit',
            kwargs={'pk': test_user.pk},
        )
        self.assertContains(response, edit_from_misago_admin_link)

        user_perms_form_data = Permission.objects.all()
        for permission in user_perms_form_data:
            self.assertContains(response, permission)
