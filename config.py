import os

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID', '')
words_db = os.environ.get('WORDS_DB_PATH', 'data/words_db.db')

BASE_DIR = os.getcwd()

ERROR_THRESHOLD = 1.0
