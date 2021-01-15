import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = os.environ['BOOPDEV_DB_URL']
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = "postgres://ofxsqguhwuapcz:967213862cd923b9ace9dca586d4e6a9eacd0b5dda5903d145b537f743f86e61@ec2-52-204-113-104.compute-1.amazonaws.com:5432/dssj73099d507"


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY