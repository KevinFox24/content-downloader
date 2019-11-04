import configparser
import os


config = configparser.ConfigParser()
config.read('../config.ini')


project_path = '/'.join(os.getcwd().split('/')[:-1])
download_directory = config.get('APP', 'download_directory')
download_path = f'{project_path}/{download_directory}/'


if not os.path.isdir("../content"):
    os.mkdir(download_path)
