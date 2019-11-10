import configparser
import os


config = configparser.ConfigParser()
config.read('../config.ini')


project_path = '/'.join(os.getcwd().split('/')[:-1])

download_directory = config.get('APP', 'download_directory')
download_path = os.path.join(project_path, download_directory)
print(download_path)

create_zip_directory = config.get('APP', 'create_zip')
create_zip_path = os.path.join('/'.join(os.getcwd().split('/')[:-1]), create_zip_directory)
print(create_zip_path)


if not os.path.isdir(f"../{download_directory}"):
    os.mkdir(download_path)

if not os.path.isdir(f"../{create_zip_directory}"):
    os.mkdir(create_zip_path)
