from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase
from misago.categories.models import Category

from misago.threads.models import Label


class LabelAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains labels link"""
        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertIn(reverse('misago:admin:categories:labels:index'),
                      response.content)

    def test_list_view(self):
        """labels list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:categories:labels:index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('No thread labels', response.content)

    def test_new_view(self):
        """new label view has no showstoppers"""
        response = self.client.get(
            reverse('misago:admin:categories:labels:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:categories:labels:new'),
            data={
                'name': 'Test Label',
                'css_class': 'test_label',
                'categories': [f.pk for f in Category.objects.all_categories()],
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:categories:labels:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Label', response.content)
        self.assertIn('test_label', response.content)

        test_label = Label.objects.get(slug='test-label')
        self.assertEqual(len(test_label.categories.all()),
                         len(Category.objects.all_categories()))
        for category in Category.objects.all_categories():
            self.assertIn(category, test_label.categories.all())

    def test_edit_view(self):
        """edit label view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:categories:labels:new'),
            data={
                'name': 'Test Label',
                'css_class': 'test_label',
                'categories': [f.pk for f in Category.objects.all_categories()],
            })
        test_label = Label.objects.get(slug='test-label')

        response = self.client.get(
            reverse('misago:admin:categories:labels:edit',
                    kwargs={'label_id': test_label.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_label.name, response.content)
        self.assertIn(test_label.css_class, response.content)

        response = self.client.post(
            reverse('misago:admin:categories:labels:edit',
                    kwargs={'label_id': test_label.pk}),
            data={
                'name': 'Top Lel',
                'css_class': 'test_lel',
                'categories': [f.pk for f in Category.objects.all_categories()],
            })
        self.assertEqual(response.status_code, 302)

        test_label = Label.objects.get(slug='top-lel')
        response = self.client.get(
            reverse('misago:admin:categories:labels:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_label.name, response.content)
        self.assertIn(test_label.css_class, response.content)

    def test_delete_view(self):
        """delete label view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:categories:labels:new'),
            data={
                'name': 'Test Label',
                'css_class': 'test_label',
                'categories': [f.pk for f in Category.objects.all_categories()],
            })
        test_label = Label.objects.get(slug='test-label')

        response = self.client.post(
            reverse('misago:admin:categories:labels:delete',
                    kwargs={'label_id': test_label.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:categories:labels:index'))
        response = self.client.get(
            reverse('misago:admin:categories:labels:index'))
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(test_label.name, response.content)
        self.assertNotIn(test_label.css_class, response.content)
