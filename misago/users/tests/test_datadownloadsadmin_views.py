import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse

from misago.admin.testutils import AdminTestCase
from misago.users.datadownloads import request_user_data_download
from misago.users.models import DataDownload


UserModel = get_user_model()

TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfiles')
TEST_FILE_PATH = os.path.join(TESTFILES_DIR, 'avatar.png')


class DataDownloadAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains data downloads link"""
        response = self.client.get(reverse('misago:admin:users:accounts:index'))

        response = self.client.get(response['location'])
        self.assertContains(response, reverse('misago:admin:users:data-downloads:index'))

    def test_list_view(self):
        """data downloads list view returns 200"""
        response = self.client.get(reverse('misago:admin:users:data-downloads:index'))
        self.assertEqual(response.status_code, 302)

        view_url = response['location']

        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)

        request_user_data_download(self.user)
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)

    def test_expire_action(self):
        """expire action marks data download as expired and deletes its file"""
        data_download = request_user_data_download(self.user)

        with open(TEST_FILE_PATH, 'rb') as upload:
            data_download.file = File(upload)
            data_download.save()

        self.assertIsNotNone(data_download.file)
        self.assertTrue(os.path.isfile(data_download.file.path))

        response = self.client.post(
            reverse('misago:admin:users:data-downloads:index'),
            data={
                'action': 'expire',
                'selected_items': [data_download.pk],
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_download.status, DataDownload.STATUS_EXPIRED)
        self.assertFalse(updated_download.file)

        self.assertFalse(os.path.isfile(data_download.file.path))

    def test_delete_action(self):
        """dele action deletes data download together with its file"""
        data_download = request_user_data_download(self.user)

        with open(TEST_FILE_PATH, 'rb') as upload:
            data_download.file = File(upload)
            data_download.save()

        self.assertIsNotNone(data_download.file)
        self.assertTrue(os.path.isfile(data_download.file.path))

        response = self.client.post(
            reverse('misago:admin:users:data-downloads:index'),
            data={
                'action': 'delete',
                'selected_items': [data_download.pk],
            },
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DataDownload.objects.count(), 0)
        self.assertFalse(os.path.isfile(data_download.file.path))

    def test_request_view(self):
        """request data downloads view initializes new downloads"""
        response = self.client.get(reverse('misago:admin:users:data-downloads:request'))
        self.assertEqual(response.status_code, 200)

        other_user = UserModel.objects.create_user('bob', 'bob@boberson.com')

        response = self.client.post(
            reverse('misago:admin:users:data-downloads:request'),
            data={
                'user_identifiers': '\n'.join([
                    self.user.username,
                    other_user.email,
                ]),
            },
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DataDownload.objects.count(), 2)

    def test_request_view_empty_data(self):
        """request data downloads view handles empty data"""
        response = self.client.get(reverse('misago:admin:users:data-downloads:request'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:data-downloads:request'),
            data={'user_identifiers': ''},
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(DataDownload.objects.count(), 0)

    def test_request_view_user_not_found(self):
        """request data downloads view handles empty data"""
        response = self.client.get(reverse('misago:admin:users:data-downloads:request'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:data-downloads:request'),
            data={'user_identifiers': 'not@found.com'},
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(DataDownload.objects.count(), 0)