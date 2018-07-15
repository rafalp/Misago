# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

from django.core.files import File

from misago.conf import settings
from misago.users.dataarchive import DataArchive
from misago.users.testutils import AuthenticatedUserTestCase


TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfiles')
TEST_AVATAR_PATH = os.path.join(TESTFILES_DIR, 'avatar.png')

DATA_DOWNLOADS_WORKING_DIR = settings.MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR


class DataArchiveTests(AuthenticatedUserTestCase):
    def test_enter_without_dirs(self):
        """data archive doesn't touch filesystem on init"""
        archive = DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR)

        self.assertEqual(archive.user, self.user)
        self.assertEqual(archive.working_dir_path, DATA_DOWNLOADS_WORKING_DIR)

        self.assertIsNone(archive.tmp_dir_path)
        self.assertIsNone(archive.data_dir_path)

    def test_context_life_cycle(self):
        """object creates valid tmp directory on enter and cleans on exit"""
        tmp_dir_path = None
        data_dir_path = None

        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            self.assertTrue(os.path.exists(archive.tmp_dir_path))
            self.assertTrue(os.path.exists(archive.data_dir_path))

            working_dir = str(DATA_DOWNLOADS_WORKING_DIR)
            tmp_dir_path = str(archive.tmp_dir_path)
            data_dir_path = str(archive.data_dir_path)
            
            self.assertTrue(tmp_dir_path.startswith(working_dir))
            self.assertTrue(data_dir_path.startswith(working_dir))

            self.assertTrue(data_dir_path.startswith(working_dir))
            self.assertTrue(data_dir_path.startswith(tmp_dir_path))

        self.assertIsNone(archive.tmp_dir_path)
        self.assertIsNone(archive.data_dir_path)

        self.assertFalse(os.path.exists(tmp_dir_path))
        self.assertFalse(os.path.exists(data_dir_path))

    def test_add_text_str(self):
        """add_dict method creates text file with string"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = u"Hello, łorld!"
            file_path = archive.add_text('testfile', data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, 'testfile.txt')
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, 'r', encoding="utf-8") as fp:
                saved_data = fp.read().strip()
                self.assertEqual(saved_data, data_to_write)

    def test_add_text_int(self):
        """add_dict method creates text file with int"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = 1234
            file_path = archive.add_text('testfile', data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, 'testfile.txt')
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, 'r', encoding="utf-8") as fp:
                saved_data = fp.read().strip()
                self.assertEqual(saved_data, str(data_to_write))

    def test_add_text_path(self):
        """add_dict method creates text file under path"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = u"Hello, łorld!"
            file_path = archive.add_text(
                'testfile', data_to_write, path=['avatars', 'tmp'])
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, 'testfile.txt')
            self.assertEqual(file_path, valid_output_path)

            data_dir_path = str(archive.data_dir_path)
            self.assertTrue(str(valid_output_path).startswith(data_dir_path))
            self.assertIn('/avatars/tmp/', str(valid_output_path))

    def test_add_dict(self):
        """add_dict method creates text file from dict"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = {'first': u"łorld!", 'second': u"łup!"}
            file_path = archive.add_dict('testfile', data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, 'testfile.txt')
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, 'r', encoding="utf-8") as fp:
                saved_data = fp.read().strip()
                self.assertEqual(saved_data, u"first: łorld!\nsecond: łup!")

    def test_add_dict_ordered(self):
        """add_dict method creates text file form ordered dict"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = OrderedDict((('first', u"łorld!"), ('second', u"łup!")))
            file_path = archive.add_dict('testfile', data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, 'testfile.txt')
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, 'r', encoding="utf-8") as fp:
                saved_data = fp.read().strip()
                self.assertEqual(saved_data, u"first: łorld!\nsecond: łup!")

    def test_add_dict_path(self):
        """add_dict method creates text file under path"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = {'first': u"łorld!", 'second': u"łup!"}
            file_path = archive.add_dict(
                'testfile', data_to_write, path=['avatars', 'tmp']))
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, 'testfile.txt')
            self.assertEqual(file_path, valid_output_path)

            data_dir_path = str(archive.data_dir_path)
            self.assertTrue(str(valid_output_path).startswith(data_dir_path))
            self.assertIn('/avatars/tmp/', str(valid_output_path))

    def test_add_model_file(self):
        """add_model_file method adds model file"""
        with open(TEST_AVATAR_PATH, 'rb') as avatar:
            self.user.avatar_tmp = File(avatar)
            self.user.save()

        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            file_path = archive.add_model_file(self.user.avatar_tmp)

            self.assertTrue(os.path.isfile(file_path))
    
            data_dir_path = str(archive.data_dir_path)
            self.assertTrue(str(file_path).startswith(data_dir_path))

    def test_add_model_file_empty(self):
        """add_model_file method is noop if model field is empty"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            file_path = archive.add_model_file(self.user.avatar_tmp)

            self.assertIsNone(file_path)
            self.assertFalse(os.listdir(archive.data_dir_path))

    def test_add_model_file_path(self):
        """add_model_file method adds model file under path"""
        with open(TEST_AVATAR_PATH, 'rb') as avatar:
            self.user.avatar_tmp = File(avatar)
            self.user.save()

        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            file_path = archive.add_model_file(
                self.user.avatar_tmp, path=['avatars', 'tmp'])

            self.assertTrue(os.path.isfile(file_path))
    
            data_dir_path = str(archive.data_dir_path)
            self.assertTrue(str(file_path).startswith(data_dir_path))
            self.assertIn('/avatars/tmp/', str(file_path))

    def test_get_file(self):
        """get_file returns django file"""
        django_file = None
        
        with open(TEST_AVATAR_PATH, 'rb') as avatar:
            self.user.avatar_tmp = File(avatar)
            self.user.save()

        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            archive.add_model_file(self.user.avatar_tmp)

            django_file = archive.get_file()
            archive_path = archive.file_path

            self.assertIsNotNone(archive_path)
            self.assertEqual(django_file.name, archive.file_path)
            self.assertFalse(django_file.closed)

        self.assertIsNone(archive.file)
        self.assertIsNone(archive.file_path)
        self.assertTrue(django_file.closed)
