"""
Congigure different environments
"""
from models.constants import (
    JWT_SECRET_KEY,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USE_TLS,
    MAIL_USE_SSL,
    MAIL_USERNAME,
    MAIL_PASSWORD
)

class Config():
    DEBUG = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_SECRET_KEY = JWT_SECRET_KEY

    MAIL_SERVER=MAIL_SERVER
    MAIL_PORT=MAIL_PORT
    MAIL_USE_TLS=MAIL_USE_TLS
    MAIL_USE_SSL=MAIL_USE_SSL
    MAIL_USERNAME=MAIL_USERNAME
    MAIL_PASSWORD=MAIL_PASSWORD



    


class DevelopmentConfig(Config):
    DEBUG =  True
    

class TestingConfig(Config):
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False



app_config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}