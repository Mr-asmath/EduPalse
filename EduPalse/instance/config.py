import os

class Config:
    SECRET_KEY = '8152910e735aacdce1f3e1707c69b49e290c726c8a06bfde00cfec5419f5f683'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school.db'  # switch to PostgreSQL in prod
    SQLALCHEMY_TRACK_MODIFICATIONS = False
