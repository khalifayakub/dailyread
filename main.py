import telebot
import time
from threading import Thread
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
            bot.get_updates(offset=-1)
            print(f"Bot polling error: {e}")
            time.sleep(15)

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    initialize_bot()
    # load_initial_links()
    
    # Start bot polling in a separate thread
    polling_thread = Thread(target=bot_polling)
    polling_thread.daemon = True
    polling_thread.start()
    
    # Start Flask in the main thread
    print("Bot is running...")
    run_flask()