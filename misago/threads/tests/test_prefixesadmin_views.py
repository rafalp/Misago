from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase
from misago.forums.models import Forum

from misago.threads.models import Prefix


class PrefixAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains prefixes link"""
        response = self.client.get(
            reverse('misago:admin:forums:nodes:index'))
        self.assertIn(reverse('misago:admin:forums:prefixes:index'),
                      response.content)

    def test_list_view(self):
        """prefixes list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:forums:prefixes:index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('No thread prefixes', response.content)

    def test_new_view(self):
        """new prefix view has no showstoppers"""
        response = self.client.get(
            reverse('misago:admin:forums:prefixes:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:forums:prefixes:new'),
            data={
                'name': 'Test Prefix',
                'css_class': 'test_prefix',
                'forums': [f.pk for f in Forum.objects.all_forums()],
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:forums:prefixes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Prefix', response.content)
        self.assertIn('test_prefix', response.content)

        test_prefix = Prefix.objects.get(slug='test-prefix')
        self.assertEqual(len(test_prefix.forums.all()),
                         len(Forum.objects.all_forums()))
        for forum in Forum.objects.all_forums():
            self.assertIn(forum, test_prefix.forums.all())

    def test_edit_view(self):
        """edit prefix view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:forums:prefixes:new'),
            data={
                'name': 'Test Prefix',
                'css_class': 'test_prefix',
                'forums': [f.pk for f in Forum.objects.all_forums()],
            })
        test_prefix = Prefix.objects.get(slug='test-prefix')

        response = self.client.get(
            reverse('misago:admin:forums:prefixes:edit',
                    kwargs={'prefix_id': test_prefix.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_prefix.name, response.content)
        self.assertIn(test_prefix.css_class, response.content)

        response = self.client.post(
            reverse('misago:admin:forums:prefixes:edit',
                    kwargs={'prefix_id': test_prefix.pk}),
            data={
                'name': 'Top Lel',
                'css_class': 'test_lel',
                'forums': [f.pk for f in Forum.objects.all_forums()],
            })
        self.assertEqual(response.status_code, 302)

        test_prefix = Prefix.objects.get(slug='top-lel')
        response = self.client.get(
            reverse('misago:admin:forums:prefixes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_prefix.name, response.content)
        self.assertIn(test_prefix.css_class, response.content)

    def test_delete_view(self):
        """delete prefix view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:forums:prefixes:new'),
            data={
                'name': 'Test Prefix',
                'css_class': 'test_prefix',
                'forums': [f.pk for f in Forum.objects.all_forums()],
            })
        test_prefix = Prefix.objects.get(slug='test-prefix')

        response = self.client.post(
            reverse('misago:admin:forums:prefixes:delete',
                    kwargs={'prefix_id': test_prefix.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:forums:prefixes:index'))
        response = self.client.get(
            reverse('misago:admin:forums:prefixes:index'))
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(test_prefix.name, response.content)
        self.assertNotIn(test_prefix.css_class, response.content)
