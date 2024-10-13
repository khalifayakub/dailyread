import os
import telebot
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Token and Chat ID from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# Test mode from environment variable
TEST_MODE = os.getenv('TEST_MODE', 'false').lower() in ('true', '1', 'yes')

# File to store links
LINKS_FILE = 'reports.txt'

bot = telebot.TeleBot(TOKEN)

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
    
    try:
        bot.send_message(CHAT_ID, message)
        print(f"Sent {len(links_to_send)} links.")

        with open(LINKS_FILE, 'w') as file:
            file.write("\n".join(remaining_links))
        print(f"Updated {LINKS_FILE} with remaining links.")
    except Exception as e:
        print(f"Error sending message: {e}")


def main():
    if not TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in environment variables.")
        return

    print("Starting Link Sender...")
    
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