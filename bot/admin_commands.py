from telebot import TeleBot
from database.mongodb import get_daily_reports, delete_sent_reports, save_daily_reports, get_all_users
from utils.helpers import format_reports
from config import ADMIN_USER_ID

def register_admin_commands(bot: TeleBot):
    @bot.message_handler(commands=['refresh'])
    def handle_refresh(message):
        if message.from_user.id != ADMIN_USER_ID:
            bot.reply_to(message, "You are not authorized to use this command.")
            return

        reports = get_daily_reports()
        if not reports:
            bot.reply_to(message, "No reports available to send.")
            return

        save_daily_reports(reports)
        delete_sent_reports()

        users = get_all_users()
        for user_id in users:
            try:
                bot.send_message(user_id, format_reports(reports))
            except Exception as e:
                print(f"Error sending message to user {user_id}: {e}")

        bot.reply_to(message, f"Sent {len(reports)} reports to {len(users)} users.")