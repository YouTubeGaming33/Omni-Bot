import os

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("No MongoDB URI Found in Environment")

client = MongoClient(MONGO_URI)
db = client["omni-bot"]
warning = db["warning"]

# Add Warning Function
def add_warning(guild_id: int, user_id: int, reason: str):
    warning.insert_one({"guild_id": guild_id, "user_id": user_id, "reason": reason})

# Fetch Warnings Function
def get_all_warnings(guild_id: int, user_id: int):
    data = warning.find({"guild_id": guild_id, "user_id": user_id})
    return [doc["reason"] for doc in data]

# Remove Warning Function
def remove_warning(guild_id: int, user_id: int):
    warning.delete_one({"guild_id": guild_id, "user_id": user_id})
    return True
