import yaml
db_conf = yaml.safe_load(open('db.yaml'))


class Config:
    SECRET_KEY = 'hardsecretkey'

    mysql_user = db_conf['mysql_user']
    mysql_password = db_conf['mysql_password']
    mysql_host = db_conf['mysql_host']
    mysql_port = db_conf['mysql_port']
    mysql_db = db_conf['mysql_db']

    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/max_database'
    SQLALCHEMY_DATABASE_URI = f'mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
