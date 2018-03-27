import os

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zxz521@localhost:3306/zlktqa?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False