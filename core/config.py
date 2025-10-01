import discord
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") # Replace with .env later.
REDDIT_C_ID: str = os.getenv("REDDIT_C_ID")
REDDIT_C_SECRET: str = os.getenv("REDDIT_C_SECRET")

GUILD_ID = discord.Object(id=1420885374758293616) #The testing server id.

DEVS = [901913992434434128, 697528564358184991]