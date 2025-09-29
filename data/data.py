import os
import uuid

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("No MongoDB URI Found in Environment")

client = MongoClient(MONGO_URI)
db = client["omni-bot"]
warning = db["warning"]
settings = db["settings"]

# Create a Unique Case Number Function
def get_case_number():
    return str(uuid.uuid4())[:8]

# Add Warning Function
def add_warning(guild_id: int, user_id: int, reason: str, caseNum: str):
    warning.insert_one({"guild_id": guild_id, "user_id": user_id, "reason": reason, "caseNum": caseNum})

# Fetch Warnings Function
def get_all_warnings(guild_id: int, user_id: int):
    data = warning.find({"guild_id": guild_id, "user_id": user_id})
    return [doc["reason"] for doc in data]

# Remove Warning Function
def remove_warning(guild_id: int, user_id: int):
    warning.delete_one({"guild_id": guild_id, "user_id": user_id})
    return True

# Toggle Guild Setting Function
def toggle_guild_setting(guild_id: int, setting: str) -> bool:
    guild = settings.find_one({"guild_id": guild_id}, {setting: 1})
    
    if not guild:
        raise ValueError(f"No guild found with id {guild_id}")
    
    current_value = guild.get(setting, 0)
    new_value = 0 if current_value else 1

    settings.update_one(
        {"guild_id": guild_id},
        {"$set": {setting: new_value}}
    )
    
    return bool(new_value)

# Add Guild to Settings Database Function
def add_guild_settings(guild_id: int):
    settings.insert_one({"guild_id": guild_id, "welcome": 0, "logging": 0})