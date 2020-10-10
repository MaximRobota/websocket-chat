import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = 'hardsecretkey'

    mysql_user = os.getenv("MYSQL_USER")
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_port = os.getenv('MYSQL_PORT')
    mysql_db = os.getenv('MYSQL_DB')

    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3399/max_database'
    SQLALCHEMY_DATABASE_URI = f'mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


print(f"Using database: {Config.SQLALCHEMY_DATABASE_URI}")
