import os
from dotenv import load_dotenv

load_dotenv()

def __getattr__(key):
    return os.getenv(key.upper())

postgres_url = os.getenv('DATABASE_URL')
postgres_params = {
    'drivername': os.getenv('POSTGRES_DRIVER'),
    'username': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('HOST', default='0.0.0.0'),
    'database': os.getenv('POSTGRES_NAME'),
    'port': os.getenv('POSTGRES_PORT', default='5432')
}

redis_url = os.getenv('REDIS_URL')
redis_params = {
    'host': os.getenv('HOST', default='0.0.0.0'),
    'port': os.getenv('REDIS_PORT', default='6379')
}
