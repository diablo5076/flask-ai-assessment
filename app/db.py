import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "flask_ai_assessment")

client = MongoClient(MONGODB_URI)

db = client[MONGODB_DB]

prompts_collection = db["prompts"]
history_collection = db["history"]


def check_database_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False