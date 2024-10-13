import os
import telebot
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Load environment variables
load_dotenv()

# Telegram Bot Token from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Test mode from environment variable
TEST_MODE = os.getenv('TEST_MODE', 'false').lower() in ('true', '1', 'yes')

# File to store links
LINKS_FILE = 'reports.txt'

# File to store user IDs
USERS_FILE = 'users.txt'

# File to store current day's links
CURRENT_DAY_LINKS_FILE = 'current_day_links.txt'

bot = telebot.TeleBot(TOKEN)

# Flask app for health check
app = Flask(__name__)

@app.route('/')
def health_check():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def get_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as file:
        return [int(line.strip()) for line in file if line.strip()]

def add_user(user_id):
    users = get_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, 'w') as file:
            for user in users:
                file.write(f"{user}\n")

@bot.message_handler(commands=['start'])
def handle_start(message):
    add_user(message.from_user.id)
    bot.reply_to(message, "Welcome! You've been added to the list to receive daily links. Use /request to get today's links.")

@bot.message_handler(commands=['request'])
def handle_request(message):
    if os.path.exists(CURRENT_DAY_LINKS_FILE):
        with open(CURRENT_DAY_LINKS_FILE, 'r') as file:
            links = file.read().strip()
        if links:
            bot.send_message(message.chat.id, f"Here are today's links:\n\n{links}")
        else:
            bot.send_message(message.chat.id, "No links have been sent today yet.")
    else:
        bot.send_message(message.chat.id, "No links have been sent today yet.")

def send_links():
    if not os.path.exists(LINKS_FILE):
        print(f"File {LINKS_FILE} not found.")
        return

    with open(LINKS_FILE, 'r') as file:
        links = file.readlines()

    links = [link.strip() for link in links if link.strip()]

    if not links:
        print("No links to send.")
        return

    links_to_send = links[:10]
    remaining_links = links[10:]

    message = "Here are your 10 links for today:\n\n" + "\n".join(links_to_send)
    
    # Save current day's links
    with open(CURRENT_DAY_LINKS_FILE, 'w') as file:
        file.write("\n".join(links_to_send))
    
    users = get_users()
    successful_sends = 0

    for user_id in users:
        try:
            bot.send_message(user_id, message)
            successful_sends += 1
        except Exception as e:
            print(f"Error sending message to user {user_id}: {e}")

    print(f"Sent links to {successful_sends} out of {len(users)} users.")

    with open(LINKS_FILE, 'w') as file:
        file.write("\n".join(remaining_links))
    print(f"Updated {LINKS_FILE} with remaining links.")

def main():
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set in environment variables.")
        return

    print("Starting Link Sender...")
    
    # Start Flask in a separate thread
    Thread(target=run_flask).start()
    
    # Start the bot polling in a separate thread
    Thread(target=bot.polling, kwargs={"none_stop": True}).start()
    
    if TEST_MODE:
        print("Running in test mode. Sending links immediately.")
        send_links()
    else:
        print("Running in scheduled mode.")
        schedule.every().day.at("09:00").do(send_links)  # Schedule to run at 9 AM daily
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()