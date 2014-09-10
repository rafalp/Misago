from django.test import TestCase


from misago.threads.views.generic.threads import Sorting


class SortingTests(TestCase):
    def setUp(self):
        self.sorting = Sorting('misago:forum', {
            'forum_slug': "test-forum",
            'forum_id': 42,
        })

    def test_clean_kwargs_removes_default_sorting(self):
        """clean_kwargs removes default sorting"""
        default_sorting = self.sorting.sortings[0]['method']

        cleaned_kwargs = self.sorting.clean_kwargs({'sort': default_sorting})
        cleaned_kwargs['pie'] = 'yum-yum'
        self.assertEqual(cleaned_kwargs, {'pie': 'yum-yum'})

    def test_clean_kwargs_removes_invalid_sorting(self):
        """clean_kwargs removes invalid sorting"""
        default_sorting = self.sorting.sortings[0]['method']

        cleaned_kwargs = self.sorting.clean_kwargs({'sort': 'bad-sort'})
        cleaned_kwargs['pie'] = 'yum-yum'
        self.assertEqual(cleaned_kwargs, {'pie': 'yum-yum'})

    def test_clean_kwargs_preserves_valid_sorting(self):
        """clean_kwargs preserves valid sorting"""
        default_sorting = self.sorting.sortings[0]['method']

        cleaned_kwargs = self.sorting.clean_kwargs({'sort': 'oldest'})
        cleaned_kwargs['pie'] = 'yum-yum'
        self.assertEqual(cleaned_kwargs, {'sort': 'oldest', 'pie': 'yum-yum'})

    def test_set_sorting_sets_valid_method(self):
        """set_sorting sets valid sorting"""
        for sorting in self.sorting.sortings:
            self.sorting.set_sorting(sorting['method'])
            self.assertEqual(sorting, self.sorting.sorting)
            self.assertEqual(sorting['name'], self.sorting.name)

    def test_choices(self):
        """choices returns set of valid choices"""
        for sorting in self.sorting.sortings:
            self.sorting.set_sorting(sorting['method'])
            choices = [choice['name'] for choice in self.sorting.choices()]
            self.assertNotIn(sorting['name'], choices)

            for other_sorting in self.sorting.sortings:
                if other_sorting != sorting:
                    self.assertIn(other_sorting['name'], choices)
