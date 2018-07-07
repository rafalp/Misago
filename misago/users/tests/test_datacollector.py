# -*- coding: utf-8 -*-
import os

from django.core.files import File

from misago.conf import settings
from misago.users.datacollector import DataCollector
from misago.users.testutils import AuthenticatedUserTestCase


TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfiles')
TEST_AVATAR_PATH = os.path.join(TESTFILES_DIR, 'avatar.png')

DATA_DOWNLOADS_WORKING_DIR = settings.MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR


class DataCollectorTests(AuthenticatedUserTestCase):
    def test_init_with_dirs(self):
        """data collector initializes with valid tmp directories"""
        data_collector = DataCollector(self.user, DATA_DOWNLOADS_WORKING_DIR)
        self.assertTrue(os.path.exists(data_collector.tmp_dir_path))
        self.assertTrue(os.path.exists(data_collector.data_dir_path))

        data_downloads_working_dir = str(DATA_DOWNLOADS_WORKING_DIR)
        tmp_dir_path = str(data_collector.tmp_dir_path)
        data_dir_path = str(data_collector.data_dir_path)
        
        self.assertTrue(tmp_dir_path.startswith(data_downloads_working_dir))
        self.assertTrue(data_dir_path.startswith(data_downloads_working_dir))

        self.assertTrue(data_dir_path.startswith(data_downloads_working_dir))
        self.assertTrue(data_dir_path.startswith(tmp_dir_path))

    def test_write_data_file(self):
        """write_data_file creates new data file in data_dir_path"""
        data_collector = DataCollector(self.user, DATA_DOWNLOADS_WORKING_DIR)

        data_to_write = {'hello': "I am test!", 'nice': u"łał!"}
        data_file_path = data_collector.write_data_file("testfile", data_to_write)
        self.assertTrue(os.path.isfile(data_file_path))

        valid_output_path = os.path.join(data_collector.data_dir_path, 'testfile.txt')
        self.assertEqual(data_file_path, valid_output_path)

        with open(data_file_path, 'r') as fp:
            saved_data = fp.read().strip().splitlines()
            self.assertEqual(saved_data, ["hello: I am test!", u"nice: łał!"])

    def test_write_model_file(self):
        """write_model_file includes model file in data_dir_path"""
        with open(TEST_AVATAR_PATH, 'rb') as avatar:
            self.user.avatar_tmp = File(avatar)
            self.user.save()

        data_collector = DataCollector(self.user, DATA_DOWNLOADS_WORKING_DIR)
        file_path = data_collector.write_model_file(self.user.avatar_tmp)
        
        self.assertTrue(os.path.isfile(file_path))
    
        data_dir_path = str(data_collector.data_dir_path)
        self.assertTrue(str(file_path).startswith(data_dir_path))

    def test_write_model_file_empty(self):
        """write_model_file is noop if model file field is none"""
        data_collector = DataCollector(self.user, DATA_DOWNLOADS_WORKING_DIR)
        file_path = data_collector.write_model_file(self.user.avatar_tmp)
        
        self.assertIsNone(file_path)
        self.assertFalse(os.listdir(data_collector.data_dir_path))