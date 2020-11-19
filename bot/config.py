import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
server_id = os.getenv('SERVER_ID')
verification_channel = os.getenv('VERIFICATION_CHANNEL')
verification_rules_channel = os.getenv('VERIFICATION_RULES_CHANNEL')
bot_id = os.getenv('BOT_ID')
cs_channel = os.getenv('CS_CHANNEL')
engineering_channel = os.getenv('ENGINEERING_CHANNEL')
stfuuuuu_aunk = os.getenv('STFUUUUU_AUNK')
verified_role = os.getenv('VERIFIED_ROLE')
postgres_url = os.getenv('DATABASE_URL')
postgres_params = {
    'drivername': os.getenv('POSTGRES_DRIVER'),
    'username': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST', default='0.0.0.0'),
    'database': os.getenv('POSTGRES_NAME'),
    'port': os.getenv('POSTGRES_PORT', default='5432')
}
redis_tls_url = os.getenv('REDIS_TLS_URL')
redis_url = os.getenv('REDIS_URL')