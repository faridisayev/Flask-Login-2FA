import os, random, string

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False