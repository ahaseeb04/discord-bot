import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
server_id = os.getenv('SERVER_ID')
verification_channel = os.getenv('VERIFICATION_CHANNEL')
verification_rules_channel = os.getenv('VERIFICATION_RULES_CHANNEL')
cs_channel = os.getenv('CS_CHANNEL')
bot_id = os.getenv('BOT_ID')
