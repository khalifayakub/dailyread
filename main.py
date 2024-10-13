import telebot
from threading import Thread
from config import TELEGRAM_BOT_TOKEN
from bot import register_commands, register_admin_commands
from database import save_links_to_db
from utils.flask_app import run_flask

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def initialize_bot():
    register_commands(bot)
    register_admin_commands(bot)

def load_initial_links():
    with open('reports.txt', 'r') as file:
        links = [line.strip() for line in file if line.strip()]
    save_links_to_db(links)
    print(f"Loaded {len(links)} links into the database.")

if __name__ == "__main__":
    initialize_bot()
    # load_initial_links()
    
    # Start Flask in a separate thread
    Thread(target=run_flask).start()
    
    print("Bot is running...")
    bot.polling(none_stop=True)