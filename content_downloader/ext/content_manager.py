import os
import shutil


class ContentManager:

    def __init__(self, download_path, zip_path):
        self._download_path: str = download_path
        self._zip_path: str = zip_path

    def create_and_get_content_dir(self, dir_name):
        path = os.path.join(self._download_path, dir_name)
        os.mkdir(path)
        return path

    def delete_content_dir(self, dir_name):
        path = os.path.join(self._download_path, dir_name)
        shutil.rmtree(path)

    def zipify_content(self, path_from, zip_name):
        path_to = self._zip_path + '/' + zip_name
        shutil.make_archive(path_to, 'zip', path_from)
        return path_to + '.zip'
