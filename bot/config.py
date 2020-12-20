from os import getenv as env
from dotenv import load_dotenv

load_dotenv()

def __getattr__(key):
    return env(key.upper())

postgres_url = env('DATABASE_URL')
postgres_params = {
    'drivername': env('POSTGRES_DRIVER'),
    'username': env('POSTGRES_USER'),
    'password': env('POSTGRES_PASSWORD'),
    'host': env('HOST', default='0.0.0.0'),
    'database': env('POSTGRES_NAME'),
    'port': env('POSTGRES_PORT', default='5432')
}

redis_url = env('REDIS_URL')
redis_params = {
    'host': env('HOST', default='0.0.0.0'),
    'port': env('REDIS_PORT', default='6379')
}
