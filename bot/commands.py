from telebot import TeleBot
from database.mongodb import add_user, get_latest_daily_reports
from utils.helpers import format_reports

def register_commands(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = message.from_user.id
        if add_user(user_id):
            bot.reply_to(message, "Welcome! You've been added to the list to receive daily reports.")
        else:
            bot.reply_to(message, "You are already in the list to receive daily reports.")

    @bot.message_handler(commands=['request'])
    def handle_request(message):
        reports = get_latest_daily_reports()
        if reports:
            bot.send_message(message.chat.id, format_reports(reports))
        else:
            bot.send_message(message.chat.id, "No reports have been sent today yet.")