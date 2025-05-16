import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '45.132.157.154'),
    'user': os.getenv('DB_USER', 'u450724067_iX9ab'),
    'password': os.getenv('DB_PASSWORD', 'IxGLaj3MJp'),
    'database': os.getenv('DB_NAME', 'u450724067_oZCJ5'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'ssl_disabled': os.getenv('DB_SSL', 'false').lower() == 'true'
}
