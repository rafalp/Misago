from django.urls import reverse

from ...acl.test import patch_user_acl
from ..test import AuthenticatedUserTestCase, create_test_user


class UserDetailsApiTests(AuthenticatedUserTestCase):
    def test_api_has_no_showstoppers(self):
        """api outputs response for freshly created user"""
        response = self.client.get(
            reverse("misago:api:user-details", kwargs={"pk": self.user.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["edit"])

    def test_api_has_no_showstoppers_old_user(self):
        """api outputs response for freshly created user"""
        self.user.profile_fields = {
            "gender": "f",
            "bio": "Lorem ipsum dolor met, sit amet elit, si vis pacem bellum.",
        }
        self.user.save()

        response = self.client.get(
            reverse("misago:api:user-details", kwargs={"pk": self.user.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["edit"])

    def test_other_user(self):
        """api handles scenario when its other user looking at profile"""
        user = create_test_user("OtherUser", "otheruser@example.com")
        api_link = reverse("misago:api:user-details", kwargs={"pk": user.pk})

        # moderator has permission to edit details
        with patch_user_acl({"can_moderate_profile_details": True}):
            response = self.client.get(api_link)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()["edit"])

        # non-moderator has no permission to edit details
        with patch_user_acl({"can_moderate_profile_details": False}):
            response = self.client.get(api_link)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.json()["edit"])

    def test_nonexistant_user(self):
        """api handles nonexistant users"""
        api_link = reverse("misago:api:user-details", kwargs={"pk": self.user.pk + 123})

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)
