import telebot
import time
from telebot.util import WorkerThread
from flask import Flask
from config import TELEGRAM_BOT_TOKEN
from bot import register_commands, register_admin_commands
from database import save_links_to_db

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "OK", 200

def initialize_bot():
    register_commands(bot)
    register_admin_commands(bot)

def load_initial_links():
    with open('reports.txt', 'r') as file:
        links = [line.strip() for line in file if line.strip()]
    save_links_to_db(links)
    print(f"Loaded {len(links)} links into the database.")

def bot_polling():
    while True:
        try:
            print("Starting bot polling...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Bot polling error: {e}")
            time.sleep(15)

if __name__ == "__main__":
    initialize_bot()
    load_initial_links()
    
    # Start bot polling in a separate thread
    worker = WorkerThread(bot_polling)
    worker.start()
    
    print("Bot is running...")
    # Run Flask app
    app.run(host='0.0.0.0', port=8080)