import os
from collections import OrderedDict

from django.core.files import File
from django.test import TestCase
from django.utils import timezone

from ...conf import settings
from ..datadownloads.dataarchive import (
    FILENAME_MAX_LEN,
    DataArchive,
    trim_long_filename,
)
from ..test import AuthenticatedUserTestCase

DATA_DOWNLOADS_WORKING_DIR = settings.MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR
TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
TEST_AVATAR_PATH = os.path.join(TESTFILES_DIR, "avatar.png")


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
            data_to_write = "Hello, łorld!"
            file_path = archive.add_text("testfile", data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, "testfile.txt")
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, "r") as fp:
                saved_data = fp.read().strip()
                self.assertEqual(saved_data, data_to_write)

    def test_add_text_int(self):
        """add_dict method creates text file with int"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = 1234
            file_path = archive.add_text("testfile", data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, "testfile.txt")
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, "r") as fp:
                saved_data = fp.read().strip()
                self.assertEqual(saved_data, str(data_to_write))

    def test_add_dict(self):
        """add_dict method creates text file from dict"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = {"first": "łorld!", "second": "łup!"}
            file_path = archive.add_dict("testfile", data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, "testfile.txt")
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, "r") as fp:
                saved_data = fp.read().strip()
                # order of dict items in py<3.6 is non-deterministic
                # making testing for exact match a mistake
                self.assertIn("first: łorld!", saved_data)
                self.assertIn("second: łup!", saved_data)

    def test_add_dict_ordered(self):
        """add_dict method creates text file form ordered dict"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            data_to_write = OrderedDict((("first", "łorld!"), ("second", "łup!")))
            file_path = archive.add_dict("testfile", data_to_write)
            self.assertTrue(os.path.isfile(file_path))

            valid_output_path = os.path.join(archive.data_dir_path, "testfile.txt")
            self.assertEqual(file_path, valid_output_path)

            with open(file_path, "r") as fp:
                saved_data = fp.read().strip()
                self.assertEqual(saved_data, "first: łorld!\nsecond: łup!")

    def test_add_model_file(self):
        """add_model_file method adds model file"""
        with open(TEST_AVATAR_PATH, "rb") as avatar:
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

    def test_add_model_file_prefixed(self):
        """add_model_file method adds model file with prefix"""
        with open(TEST_AVATAR_PATH, "rb") as avatar:
            self.user.avatar_tmp = File(avatar)
            self.user.save()

        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            file_path = archive.add_model_file(self.user.avatar_tmp, prefix="prefix")

            self.assertTrue(os.path.isfile(file_path))

            data_dir_path = str(archive.data_dir_path)
            self.assertTrue(str(file_path).startswith(data_dir_path))

            filename = os.path.basename(self.user.avatar_tmp.name)
            target_filename = "prefix-%s" % filename
            self.assertTrue(str(file_path).endswith(target_filename))

    def test_make_final_path_no_kwargs(self):
        """make_final_path returns data_dir_path if no kwargs are set"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            final_path = archive.make_final_path()
            self.assertEqual(final_path, archive.data_dir_path)

    def test_make_final_path_directory(self):
        """make_final_path returns path including directory name"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            final_path = archive.make_final_path(directory="test-directory")
            valid_path = os.path.join(archive.data_dir_path, "test-directory")
            self.assertEqual(final_path, valid_path)

    def test_make_final_path_date(self):
        """make_final_path returns path including date segments"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            now = timezone.now().date()
            final_path = archive.make_final_path(date=now)

            valid_path = os.path.join(
                archive.data_dir_path,
                now.strftime("%Y"),
                now.strftime("%m"),
                now.strftime("%d"),
            )

            self.assertEqual(final_path, valid_path)

    def test_make_final_path_datetime(self):
        """make_final_path returns path including date segments"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            now = timezone.now()
            final_path = archive.make_final_path(date=now)

            valid_path = os.path.join(
                archive.data_dir_path,
                now.strftime("%Y"),
                now.strftime("%m"),
                now.strftime("%d"),
            )

            self.assertEqual(final_path, valid_path)

    def test_make_final_path_both_kwargs(self):
        """make_final_path raises value error if both date and directory are set"""
        with DataArchive(self.user, DATA_DOWNLOADS_WORKING_DIR) as archive:
            expected_message = "date and directory arguments are mutually exclusive"
            with self.assertRaisesMessage(ValueError, expected_message):
                archive.make_final_path(date=timezone.now(), directory="test")

    def test_get_file(self):
        """get_file returns django file"""
        django_file = None

        with open(TEST_AVATAR_PATH, "rb") as avatar:
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


class TrimLongFilenameTests(TestCase):
    def test_trim_short_filename(self):
        """trim_too_long_filename returns short filename as it is"""
        filename = "filename.jpg"
        trimmed_filename = trim_long_filename(filename)
        self.assertEqual(trimmed_filename, filename)

    def test_trim_too_long_filename(self):
        """trim_too_long_filename trims filename if its longer than allowed"""
        filename = "filename"
        extension = ".jpg"
        long_filename = "%s%s" % (filename * 10, extension)

        trimmed_filename = trim_long_filename(long_filename)

        self.assertEqual(len(trimmed_filename), FILENAME_MAX_LEN)
        self.assertTrue(trimmed_filename.startswith(filename))
        self.assertTrue(trimmed_filename.endswith(extension))
