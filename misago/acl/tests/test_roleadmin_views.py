from django.urls import reverse

from .. import ACL_CACHE
from ...admin.test import AdminTestCase
from ...cache.test import assert_invalidates_cache
from ..models import Role
from ..test import mock_role_form_data


def create_data(data_dict):
    return mock_role_form_data(Role(), data_dict)


class RoleAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains user roles link"""
        response = self.client.get(reverse("misago:admin:permissions:index"))
        self.assertContains(response, reverse("misago:admin:permissions:index"))

    def test_list_view(self):
        """roles list view returns 200"""
        response = self.client.get(reverse("misago:admin:permissions:index"))
        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        """new role view has no showstoppers"""
        response = self.client.get(reverse("misago:admin:permissions:new"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("misago:admin:permissions:new"),
            data=create_data({"name": "Test Role"}),
        )
        self.assertEqual(response.status_code, 302)

        test_role = Role.objects.get(name="Test Role")
        response = self.client.get(reverse("misago:admin:permissions:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_role.name)

    def test_edit_view(self):
        """edit role view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:permissions:new"),
            data=create_data({"name": "Test Role"}),
        )

        test_role = Role.objects.get(name="Test Role")

        response = self.client.get(
            reverse("misago:admin:permissions:edit", kwargs={"pk": test_role.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Role")

        response = self.client.post(
            reverse("misago:admin:permissions:edit", kwargs={"pk": test_role.pk}),
            data=create_data({"name": "Top Lel"}),
        )
        self.assertEqual(response.status_code, 302)

        test_role = Role.objects.get(name="Top Lel")
        response = self.client.get(reverse("misago:admin:permissions:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_role.name)

    def test_editing_role_invalidates_acl_cache(self):
        self.client.post(
            reverse("misago:admin:permissions:new"),
            data=create_data({"name": "Test Role"}),
        )

        test_role = Role.objects.get(name="Test Role")

        with assert_invalidates_cache(ACL_CACHE):
            self.client.post(
                reverse("misago:admin:permissions:edit", kwargs={"pk": test_role.pk}),
                data=create_data({"name": "Top Lel"}),
            )

    def test_users_view(self):
        """users with this role view has no showstoppers"""
        response = self.client.post(
            reverse("misago:admin:permissions:new"),
            data=create_data({"name": "Test Role"}),
        )
        test_role = Role.objects.get(name="Test Role")

        response = self.client.get(
            reverse("misago:admin:permissions:users", kwargs={"pk": test_role.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        """delete role view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:permissions:new"),
            data=create_data({"name": "Test Role"}),
        )

        test_role = Role.objects.get(name="Test Role")
        response = self.client.post(
            reverse("misago:admin:permissions:delete", kwargs={"pk": test_role.pk})
        )
        self.assertEqual(response.status_code, 302)

        # Get the page twice so no alert is renderered on second request
        self.client.get(reverse("misago:admin:permissions:index"))
        response = self.client.get(reverse("misago:admin:permissions:index"))
        self.assertNotContains(response, test_role.name)

    def test_deleting_role_invalidates_acl_cache(self):
        self.client.post(
            reverse("misago:admin:permissions:new"),
            data=create_data({"name": "Test Role"}),
        )

        test_role = Role.objects.get(name="Test Role")

        with assert_invalidates_cache(ACL_CACHE):
            self.client.post(
                reverse("misago:admin:permissions:delete", kwargs={"pk": test_role.pk})
            )
