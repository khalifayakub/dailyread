from pymongo import MongoClient
from config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client['telegram_bot_db']

users_collection = db['users']
reports_collection = db['reports']
daily_reports_collection = db['daily_reports']

def save_links_to_db(links):
    reports_collection.insert_many([{"link": link} for link in links])

def get_daily_reports(count=10):
    return [report['link'] for report in reports_collection.find().limit(count)]

def delete_sent_reports(count=10):
    reports_to_delete = reports_collection.find().limit(count)
    reports_collection.delete_many({"_id": {"$in": [report['_id'] for report in reports_to_delete]}})

def save_daily_reports(reports):
    daily_reports_collection.insert_one({"reports": reports})

def get_latest_daily_reports():
    latest = daily_reports_collection.find_one(sort=[('_id', -1)])
    return latest['reports'] if latest else []

def add_user(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})
        return True
    return False

def get_all_users():
    return [user['user_id'] for user in users_collection.find()]