import os


class Config:
    SECRET_KEY = 'e2be724f76268c84d1ed12d80d784af7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.ukr.net'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('UKRNET_USER')
    MAIL_PASSWORD = os.environ.get('UKRNET_PASS')
