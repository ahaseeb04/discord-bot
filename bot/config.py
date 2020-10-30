import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER_ID = os.getenv('SERVER_ID')
VERIFICATION_CHANNEL = os.getenv('VERIFICATION_CHANNEL')
