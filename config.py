class Config:
    SECRET_KEY = '1b23d48200e2e48b4cf30dd58b8c1e405c8d7a0c963f311e'
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'finance.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:123456@localhost/exp_db'
