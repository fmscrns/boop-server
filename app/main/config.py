import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = os.environ['BOOPDEV_DB_URL']
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIN_DOMAIN = "http://127.0.0.1:8080"
    PER_PAGE_PAGINATION = 3

class ProductionConfig(Config):
    DEBUG = False
    MAIN_DOMAIN = "https://boop-proj-client.herokuapp.com"
    PER_PAGE_PAGINATION = 5
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_remote_base


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY