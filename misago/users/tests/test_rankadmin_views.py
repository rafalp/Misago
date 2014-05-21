from django.core.urlresolvers import reverse
from misago.admin.testutils import AdminTestCase
from misago.users.models import Rank


class RankAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains ranks link"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))

        self.assertIn(reverse('misago:admin:users:ranks:index'),
                      response.content)

    def test_list_view(self):
        """ranks list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:users:ranks:index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Team', response.content)


    def test_new_view(self):
        """new rank view has no showstoppers"""
        response = self.client.get(
            reverse('misago:admin:users:ranks:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:ranks:new'),
            data={
                'name': 'Test Rank',
                'description': 'Lorem ipsum dolor met',
                'title': 'Test Title',
                'style': 'test',
                'is_tab': '1',
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:users:ranks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Rank', response.content)
        self.assertIn('Test Title', response.content)


    def test_edit_view(self):
        """edit rank view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:ranks:new'),
            data={
                'name': 'Test Rank',
                'description': 'Lorem ipsum dolor met',
                'title': 'Test Title',
                'style': 'test',
                'is_tab': '1',
            })

        test_rank = Rank.objects.get(slug='test-rank')

        response = self.client.get(
            reverse('misago:admin:users:ranks:edit',
                    kwargs={'rank_id': test_rank.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Rank', response.content)
        self.assertIn('Test Title', response.content)

        response = self.client.post(
            reverse('misago:admin:users:ranks:edit',
                    kwargs={'rank_id': test_rank.pk}),
            data={'name': 'Top Lel'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:users:ranks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Top Lel', response.content)

    def test_default_view(self):
        """default rank view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:ranks:new'),
            data={
                'name': 'Test Rank',
                'description': 'Lorem ipsum dolor met',
                'title': 'Test Title',
                'style': 'test',
                'is_tab': '1',
            })

        test_rank = Rank.objects.get(slug='test-rank')

        response = self.client.post(
            reverse('misago:admin:users:ranks:default',
                    kwargs={'rank_id': test_rank.pk}))
        self.assertEqual(response.status_code, 302)

        test_rank = Rank.objects.get(slug='test-rank')
        self.assertTrue(test_rank.is_default)

    def test_move_up_view(self):
        """move rank up view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:ranks:new'),
            data={
                'name': 'Test Rank',
                'description': 'Lorem ipsum dolor met',
                'title': 'Test Title',
                'style': 'test',
                'is_tab': '1',
            })

        test_rank = Rank.objects.get(slug='test-rank')

        response = self.client.post(
            reverse('misago:admin:users:ranks:up',
                    kwargs={'rank_id': test_rank.pk}))
        self.assertEqual(response.status_code, 302)

        changed_rank = Rank.objects.get(slug='test-rank')
        self.assertEqual(changed_rank.order + 1, test_rank.order)

    def test_move_down_view(self):
        """move rank down view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:ranks:new'),
            data={
                'name': 'Test Rank',
                'description': 'Lorem ipsum dolor met',
                'title': 'Test Title',
                'style': 'test',
                'is_tab': '1',
            })

        test_rank = Rank.objects.get(slug='test-rank')

        # Move rank up
        response = self.client.post(
            reverse('misago:admin:users:ranks:up',
                    kwargs={'rank_id': test_rank.pk}))

        response = self.client.post(
            reverse('misago:admin:users:ranks:down',
                    kwargs={'rank_id': test_rank.pk}))
        self.assertEqual(response.status_code, 302)

        # Test move down
        changed_rank = Rank.objects.get(slug='test-rank')
        self.assertEqual(changed_rank.order, test_rank.order)

    def test_delete_view(self):
        """delete rank view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:ranks:new'),
            data={
                'name': 'Test Rank',
                'description': 'Lorem ipsum dolor met',
                'title': 'Test Title',
                'style': 'test',
                'is_tab': '1',
            })

        test_rank = Rank.objects.get(slug='test-rank')

        response = self.client.post(
            reverse('misago:admin:users:ranks:delete',
                    kwargs={'rank_id': test_rank.pk}))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:users:ranks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Top Lel' not in response.content)
