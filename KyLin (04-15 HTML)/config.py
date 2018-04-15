# database_type+driver://user:password@sql_server_ip:port/database_name


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:msi3861678@127.0.0.1:3306/kylin'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    CSRF_ENABLED = True
    SECRET_KEY = 'KyLin'
    DATA_PER_PAGE = 2

