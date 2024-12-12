import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'we0234t934jf2kf2w4h555t5g54g5445gh654hujjjrthtrhg4wh4')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
