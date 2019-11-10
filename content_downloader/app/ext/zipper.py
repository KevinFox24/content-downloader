import asyncio
from content_downloader.config import create_zip_path
import shutil
import os


def zipify_content(path_from, path_to=create_zip_path, name='test'):
    path_to = path_to + '/' + name
    shutil.make_archive(path_to, 'zip', path_from)
    return path_to + '.zip'


def clean_folder(path):
    shutil.rmtree(path)
    os.mkdir(path)

