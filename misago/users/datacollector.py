import json
import os
import shutil

from django.utils import timezone
from django.utils.crypto import get_random_string


class DataWriter(object):
    def write_json_file(self, name, data):
        file_path = os.path.join(self.data_dir_path, '{}.json'.format(name))
        with open(file_path, 'w+') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)

    def write_file(self, model_file):
        if not model_file:
            return None

        target_filename = model_file.name.split('/')[-1]
        target_path = os.path.join(self.data_dir_path, target_filename)

        with open(target_path, 'wb') as fp:
            for chunk in model_file.chunks():
                fp.write(chunk)

        return target_path
        

class DataCollection(DataWriter):
    def __init__(self, user, data_dir_path):
        self.user = user
        self.data_dir_path = data_dir_path
        os.mkdir(data_dir_path)


class DataCollector(DataWriter):
    def __init__(self, user, working_dir_path):
        self.user = user
        self.working_dir_path = working_dir_path

        self.archive_path = None
        self.tmp_dir_path = self.create_tmp_dir()
        self.data_dir_path = self.create_data_dir()

    def get_tmp_dir_name(self):
        dir_name_bits = [
            self.user.slug,
            timezone.now().strftime('%Y%m%d-%H%M%S'),
            get_random_string(6),
        ]

        return '-'.join(dir_name_bits)

    def create_tmp_dir(self):
        tmp_dir_name = self.get_tmp_dir_name()
        tmp_dir_path = os.path.join(self.working_dir_path, tmp_dir_name)

        os.mkdir(tmp_dir_path)

        return tmp_dir_path

    def get_data_dir_name(self):
        dir_name_bits = [
            self.user.slug,
            timezone.now().strftime('%Y%m%d-%H%M%S'),
        ]

        return '-'.join(dir_name_bits)

    def create_data_dir(self):
        data_dir_name = self.get_data_dir_name()
        data_dir_path = os.path.join(self.tmp_dir_path, data_dir_name)

        os.mkdir(data_dir_path)

        return data_dir_path

    def create_collection(self, name):
        collection_dir_path = os.path.join(self.data_dir_path, name)
        return DataCollection(self.user, collection_dir_path)

    def create_archive(self):
        archive_name = self.get_tmp_dir_name()
        archive_path = os.path.join(self.working_dir_path, archive_name)
        shutil.make_archive(archive_path, 'zip', self.tmp_dir_path)

        self.archive_path = archive_path
        return archive_path

    def delete_tmp_dir(self):
        shutil.rmtree(self.tmp_dir_path)
