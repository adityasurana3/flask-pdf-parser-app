import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    CELERY_BROKER_URL = 'redis://redis-server:6379/0'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False