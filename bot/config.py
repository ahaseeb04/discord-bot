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
database_url = os.getenv('DATABASE_URL', None)
database = {
    'drivername': os.getenv('DB_DRIVER'),
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', default='0.0.0.0'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', default='5432')
}