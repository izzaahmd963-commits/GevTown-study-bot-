# ============================================
# DATABASE CONNECTION - MongoDB
# ============================================

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI")

try:
    client = MongoClient(MONGODB_URI)
    db = client["study_bot"]
    chats_collection = db["chat_history"]
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    chats_collection = None

def save_chat(user_id, user_message, bot_response):
    """Save chat to MongoDB"""
    if chats_collection is None:
        print("⚠️ MongoDB not connected. Chat not saved.")
        return False
    
    chat_data = {
        "user_id": user_id,
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.now()
    }
    result = chats_collection.insert_one(chat_data)
    print(f"✅ Chat saved with ID: {result.inserted_id}")
    return True

def get_chat_history(user_id, limit=5):
    """Get last 5 chats for context"""
    if chats_collection is None:
        return ""
    
    history = chats_collection.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(limit)
    
    messages = []
    for chat in reversed(list(history)):
        messages.append(f"User: {chat['user_message']}")
        messages.append(f"Assistant: {chat['bot_response']}")
    
    return "\n".join(messages)

def test_connection():
    """Test MongoDB connection"""
    try:
        client.admin.command('ping')
        return True
    except:
        return False