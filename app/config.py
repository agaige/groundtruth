import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """ Base configuration. """
    WTF_CSRF_ENABLED = True
    REDIS_URL = 'redis://redis_db:6379/0'
    QUEUES = ['default']


class WorkerConfig(BaseConfig):
    """ Worker config """
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    """ Development configuration. """
    REDIS_URL = 'redis://127.0.0.1:6379/0'


