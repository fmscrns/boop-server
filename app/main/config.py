import os

# uncomment the line below for postgres database url from environment variable
postgres_local_base = os.environ['BOOPDEV_DB_URL']

# postgres_remote_base = os.environ['BOOPPROD_DB_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIN_DOMAIN = "http://127.0.0.1:8080"
    PER_PAGE_PAGINATION = 2

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