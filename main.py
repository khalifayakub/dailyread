import telebot
from flask import Flask, request
from config import TELEGRAM_BOT_TOKEN, WEBHOOK_URL_BASE, WEBHOOK_URL_PATH
from bot import register_commands, register_admin_commands
from database import save_links_to_db

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

# Webhook route
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Error: Bad request', 400

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

if __name__ == "__main__":
    initialize_bot()
    
    # Remove webhook, then set it up
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    
    print("Bot is running...")
    # Start Flask
    app.run(host='0.0.0.0', port=9999)