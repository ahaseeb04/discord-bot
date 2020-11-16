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
db = os.getenv('DB')
database = {
    'drivername': os.getenv(f'{db}_DRIVER'),
    'username': os.getenv(f'{db}_USER'),
    'password': os.getenv(f'{db}_PASSWORD'),
    'host': os.getenv(f'{db}_HOST', default='0.0.0.0'),
    'database': os.getenv(f'{db}_NAME'),
    'port': os.getenv(f'{db}_PORT', default='5432')
}