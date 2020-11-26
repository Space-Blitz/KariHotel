"""
Congigure different environments
"""
from models.constants import (
    JWT_SECRET_KEY
)

class Config():
    DEBUG = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_SECRET_KEY = JWT_SECRET_KEY

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