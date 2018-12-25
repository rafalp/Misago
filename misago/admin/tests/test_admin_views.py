from django.test import TestCase
from django.urls import reverse

from ...users.test import create_test_user
from ..test import AdminTestCase
from ..views import get_protected_namespace


class AdminViewAccessTests(AdminTestCase):
    def test_admin_denies_non_staff_non_superuser(self):
        """admin middleware rejects user thats non staff and non superuser"""
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "Sign in")

    def test_admin_denies_non_staff_superuser(self):
        """admin middleware rejects user thats non staff and superuser"""
        self.user.is_staff = False
        self.user.is_superuser = True
        self.user.save()

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "Sign in")

    def test_admin_passess_in_staff_non_superuser(self):
        """admin middleware passess user thats staff and non superuser"""
        self.user.is_staff = True
        self.user.is_superuser = False
        self.user.save()

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, self.user.username)

    def test_admin_passess_in_staff_superuser(self):
        """admin middleware passess user thats staff and superuser"""
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, self.user.username)


class Admin404ErrorTests(AdminTestCase):
    def test_list_search_unicode_handling(self):
        """querystring creation handles unicode strings"""
        test_link = "%stotally-errored/" % reverse("misago:admin:index")

        response = self.client.get(test_link)

        self.assertContains(
            response, "Requested page could not be found.", status_code=404
        )


class AdminGenericViewsTests(AdminTestCase):
    def test_view_redirected_queryvar(self):
        """querystring redirected value is handled"""
        test_link = reverse("misago:admin:users:accounts:index")

        # request resulted in redirect with redirected=1 bit
        response = self.client.get("%s?username=lorem" % test_link)
        self.assertEqual(response.status_code, 302)
        self.assertIn("redirected=1", response["location"])

        # request with flag muted redirect
        response = self.client.get("%s?redirected=1&username=lorem" % test_link)
        self.assertEqual(response.status_code, 200)

    def test_list_search_unicode_handling(self):
        """querystring creation handles unicode strings"""
        test_link = reverse("misago:admin:users:accounts:index")
        response = self.client.get("%s?redirected=1&username=%s" % (test_link, "łut"))
        self.assertEqual(response.status_code, 200)
