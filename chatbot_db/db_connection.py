import pymysql
from db_config import DB_CONFIG

def get_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        port=DB_CONFIG['port'],
        ssl_disabled=DB_CONFIG['ssl_disabled'],
        cursorclass=pymysql.cursors.DictCursor
    )
