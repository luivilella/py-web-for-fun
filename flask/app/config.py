import os


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'WU9QGQfRgv66Lv9QLtNn+eYbmuYH2EaP.Wcoy9VrmJ8nWG?r$tGapsY2EWUUHqGL'
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///tmp/test.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        os.environ.get('SQLALCHEMY_DATABASE_URI', 'true').lower() == 'true'
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
