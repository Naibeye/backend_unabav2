from os import environ, path
from dotenv import load_dotenv
import os
import json
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
class ProdConfig:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SESSION_TYPE='sqlalchemy'
    ALCHEMICAL_DATABASE_URL = environ.get('PROD_DATABASE_URI')
    SECRET=environ.get('SECRET')
    ACCESS_TOKEN_MINUTES=120
    RESET_TOKEN_MINUTES=30
    FRONTEND_URL="localhost:5000"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    # Mail Config
    STATIC_FOLDER = 'static'
    MAIL_SERVER = os.environ.get('MAIL_SERVER_UA') or ""
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME_UA') or ""
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD_UA') or ""
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # SSO Config
    SECRET_CRT = os.environ.get('SECRET_CRT') or ""
    ID_NAIBI = os.environ.get('ID_NAIBI') or ""
    CRT_NAIBI = os.environ.get('CRT_NAIBI') or ""

    # API documentation
    APIFAIRY_TITLE = 'Naibi SSO'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI = os.environ.get('DOCS_UI', 'elements')

    #MongoDB
    MONGODB_SETTINGS = [
    {
        "db": os.environ.get('PROD_DATABASE_UA') or "db_unaba",
        "host": os.environ.get('PROD_DATABASE_SERVER_UA') or "localhost",
        "port":  27017,
        "alias": "default",
    }]
    #File
    MAX_CONTENT_LENGTH = 100*1024 * 1024
    UPLOAD_IMAGE_EXTENSIONS= ['.jpg', '.jpeg','.png', '.gif']
    UPLOAD_PATH = os.path.join(basedir,'static/uploads')
    # Adminstation Init
    ADMIN_MAIL_UA=os.environ.get("ADMIN_MAIL_UA") 
    ADMIN_PASSWORD_UA=os.environ.get("ADMIN_PASSWORD_UA")