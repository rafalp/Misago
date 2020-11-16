import os
import shutil

from django.core.files import File
from django.utils import timezone
from django.utils.crypto import get_random_string

from ...core.utils import slugify

FILENAME_MAX_LEN = 50


class DataArchive:
    def __init__(self, user, working_dir_path):
        self.user = user
        self.working_dir_path = working_dir_path

        self.tmp_dir_path = None
        self.data_dir_path = None

        self.file_path = None
        self.file = None

    def __enter__(self):
        self.tmp_dir_path = self.create_tmp_dir()
        self.data_dir_path = self.create_data_dir()

        return self

    def __exit__(self, *args):
        self.delete_file()
        self.delete_tmp_dir()

    def create_tmp_dir(self):
        tmp_dir_name = get_tmp_filename(self.user)
        tmp_dir_path = os.path.join(self.working_dir_path, tmp_dir_name)

        os.mkdir(tmp_dir_path)

        return tmp_dir_path

    def create_data_dir(self):
        data_dir_name = get_tmp_filename(self.user)
        data_dir_path = os.path.join(self.tmp_dir_path, data_dir_name)

        os.mkdir(data_dir_path)

        return data_dir_path

    def delete_tmp_dir(self):
        if self.tmp_dir_path:
            shutil.rmtree(self.tmp_dir_path)
            self.tmp_dir_path = None
            self.data_dir_path = None

    def get_file(self):
        file_name = get_tmp_filename(self.user)
        file_path = os.path.join(self.working_dir_path, file_name)

        self.file_path = shutil.make_archive(file_path, "zip", self.tmp_dir_path)
        self.file = open(self.file_path, "rb")

        return File(self.file)

    def delete_file(self):
        if self.file:
            self.file.close()
            self.file = None

        if self.file_path:
            os.remove(self.file_path)
            self.file_path = None

    def add_text(self, name, value, date=None, directory=None):
        clean_filename = slugify(str(name))
        file_dir_path = self.make_final_path(date=date, directory=directory)
        file_path = os.path.join(file_dir_path, "%s.txt" % clean_filename)
        with open(file_path, "w") as fp:
            fp.write(str(value))
            return file_path

    def add_dict(self, name, value, date=None, directory=None):
        text_lines = []
        for key, item in value.items():
            text_lines.append("%s: %s" % (key, item))
        text = "\n".join(text_lines)
        return self.add_text(name, text, date=date, directory=directory)

    def add_model_file(self, model_file, prefix=None, date=None, directory=None):
        if not model_file:
            return None

        target_dir_path = self.make_final_path(date=date, directory=directory)

        filename = os.path.basename(model_file.name)
        if prefix:
            prefixed_filename = "%s-%s" % (prefix, filename)
            clean_filename = trim_long_filename(prefixed_filename)
            target_path = os.path.join(target_dir_path, clean_filename)
        else:
            clean_filename = trim_long_filename(filename)
            target_path = os.path.join(target_dir_path, clean_filename)

        with open(target_path, "wb") as fp:
            for chunk in model_file.chunks():
                fp.write(chunk)

        return target_path

    def make_final_path(self, date=None, directory=None):
        # fixme: os.path.isdir test can be avoided in py37k
        if date and directory:
            raise ValueError("date and directory arguments are mutually exclusive")

        data_dir_path = self.data_dir_path

        if date:
            final_path = data_dir_path
            path_items = [date.strftime("%Y"), date.strftime("%m"), date.strftime("%d")]
            for path_item in path_items:
                final_path = os.path.join(final_path, str(path_item))
                if not os.path.isdir(final_path):
                    os.mkdir(final_path)
            return final_path

        if directory:
            final_path = os.path.join(data_dir_path, str(directory))
            if not os.path.isdir(final_path):
                os.mkdir(final_path)
            return final_path

        return data_dir_path


def get_tmp_filename(user):
    filename_bits = [
        user.slug,
        timezone.now().strftime("%Y%m%d-%H%M%S"),
        get_random_string(6),
    ]

    return "-".join(filename_bits)


def trim_long_filename(filename):
    # fixme: consider moving this utility to better place?
    # eg. to trim too long attachment filenames on upload
    if len(filename) < FILENAME_MAX_LEN:
        return filename

    name, extension = os.path.splitext(filename)
    name_len = FILENAME_MAX_LEN - len(extension)
    return "%s%s" % (name[:name_len], extension)
