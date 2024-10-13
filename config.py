import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MONGODB_URI = os.getenv('MONGODB_URI')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))

# New webhook configurations
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')  # e.g., 'your-app-name.onrender.com'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f"/{TELEGRAM_BOT_TOKEN}/"