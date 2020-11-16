from django.urls import reverse

from ....acl import ACL_CACHE
from ....acl.models import Role
from ....admin.test import AdminTestCase
from ....cache.test import assert_invalidates_cache
from ...models import Rank


class RankAdminTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains ranks link"""
        response = self.client.get(reverse("misago:admin:users:index"))

        response = self.client.get(response["location"])
        self.assertContains(response, reverse("misago:admin:ranks:index"))

    def test_list_view(self):
        """ranks list view returns 200"""
        response = self.client.get(reverse("misago:admin:ranks:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Team")

    def test_new_view(self):
        """new rank view has no showstoppers"""
        test_role_a = Role.objects.create(name="Test Role A")
        test_role_b = Role.objects.create(name="Test Role B")
        test_role_c = Role.objects.create(name="Test Role C")

        response = self.client.get(reverse("misago:admin:ranks:new"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
                "roles": [test_role_a.pk, test_role_c.pk],
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:ranks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Rank")
        self.assertContains(response, "Test Title")

        test_rank = Rank.objects.get(slug="test-rank")
        self.assertIn(test_role_a, test_rank.roles.all())
        self.assertIn(test_role_c, test_rank.roles.all())
        self.assertTrue(test_role_b not in test_rank.roles.all())

    def test_edit_view(self):
        """edit rank view has no showstoppers"""
        test_role_a = Role.objects.create(name="Test Role A")
        test_role_b = Role.objects.create(name="Test Role B")
        test_role_c = Role.objects.create(name="Test Role C")

        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
                "roles": [test_role_a.pk, test_role_c.pk],
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        response = self.client.get(
            reverse("misago:admin:ranks:edit", kwargs={"pk": test_rank.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_rank.name)
        self.assertContains(response, test_rank.title)

        response = self.client.post(
            reverse("misago:admin:ranks:edit", kwargs={"pk": test_rank.pk}),
            data={"name": "Top Lel", "roles": [test_role_b.pk]},
        )
        self.assertEqual(response.status_code, 302)

        test_rank = Rank.objects.get(slug="top-lel")
        response = self.client.get(reverse("misago:admin:ranks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_rank.name)
        self.assertTrue("Test Rank" not in test_rank.roles.all())
        self.assertTrue("Test Title" not in test_rank.roles.all())

        self.assertIn(test_role_b, test_rank.roles.all())
        self.assertTrue(test_role_a not in test_rank.roles.all())
        self.assertTrue(test_role_c not in test_rank.roles.all())

    def test_editing_rank_invalidates_acl_cache(self):
        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")
        test_role_b = Role.objects.create(name="Test Role B")

        with assert_invalidates_cache(ACL_CACHE):
            self.client.post(
                reverse("misago:admin:ranks:edit", kwargs={"pk": test_rank.pk}),
                data={"name": "Top Lel", "roles": [test_role_b.pk]},
            )

    def test_default_view(self):
        """default rank view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        response = self.client.post(
            reverse("misago:admin:ranks:default", kwargs={"pk": test_rank.pk})
        )
        self.assertEqual(response.status_code, 302)

        test_rank = Rank.objects.get(slug="test-rank")
        self.assertTrue(test_rank.is_default)

    def test_move_up_view(self):
        """move rank up view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        response = self.client.post(
            reverse("misago:admin:ranks:up", kwargs={"pk": test_rank.pk})
        )
        self.assertEqual(response.status_code, 302)

        changed_rank = Rank.objects.get(slug="test-rank")
        self.assertEqual(changed_rank.order + 1, test_rank.order)

    def test_move_down_view(self):
        """move rank down view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        # Move rank up
        response = self.client.post(
            reverse("misago:admin:ranks:up", kwargs={"pk": test_rank.pk})
        )

        response = self.client.post(
            reverse("misago:admin:ranks:down", kwargs={"pk": test_rank.pk})
        )
        self.assertEqual(response.status_code, 302)

        # Test move down
        changed_rank = Rank.objects.get(slug="test-rank")
        self.assertEqual(changed_rank.order, test_rank.order)

    def test_users_view(self):
        """users with this rank view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        response = self.client.get(
            reverse("misago:admin:ranks:users", kwargs={"pk": test_rank.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        """delete rank view has no showstoppers"""
        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        response = self.client.post(
            reverse("misago:admin:ranks:delete", kwargs={"pk": test_rank.pk})
        )
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse("misago:admin:ranks:index"))
        response = self.client.get(reverse("misago:admin:ranks:index"))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, test_rank.name)
        self.assertNotContains(response, test_rank.title)

    def test_deleting_rank_invalidates_acl_cache(self):
        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test Rank",
                "description": "Lorem ipsum dolor met",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        with assert_invalidates_cache(ACL_CACHE):
            self.client.post(
                reverse("misago:admin:ranks:delete", kwargs={"pk": test_rank.pk})
            )

    def test_uniquess(self):
        """rank slug uniqueness is enforced by admin forms"""
        test_role_a = Role.objects.create(name="Test Role A")

        response = self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Members",
                "description": "Colliding rank",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
                "roles": [test_role_a.pk],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This name collides with other rank.")

        self.client.post(
            reverse("misago:admin:ranks:new"),
            data={
                "name": "Test rank",
                "description": "Colliding rank",
                "title": "Test Title",
                "style": "test",
                "is_tab": "1",
                "roles": [test_role_a.pk],
            },
        )

        test_rank = Rank.objects.get(slug="test-rank")

        response = self.client.post(
            reverse("misago:admin:ranks:edit", kwargs={"pk": test_rank.pk}),
            data={"name": "Members", "roles": [test_role_a.pk]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This name collides with other rank.")
