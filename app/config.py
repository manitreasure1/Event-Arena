import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SUPER_SECRET')
    SECRET_KEY= os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///event.db'
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False