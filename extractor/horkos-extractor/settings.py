import os
from config.config import Config

config = Config()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.get('HORKOS', 'datasource.url').split("/")[3].split("?")[0],
        'USER': config.get('HORKOS', 'datasource.username'),
        'PASSWORD': config.get('HORKOS', 'datasource.password'),
        'HOST': config.get('HORKOS', 'datasource.url').split("/")[2],
    }
}

INSTALLED_APPS = (
    'data',
)

SECRET_KEY = os.environ['SECRET_KEY']
