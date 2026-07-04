import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    DISK_TOKEN = os.getenv('DISK_TOKEN', '')
    DISK_HOST = os.getenv('DISK_HOST', 'https://cloud-api.yandex.net/')
    DISK_API_VERSION = os.getenv('API_VERSION', 'v1')
