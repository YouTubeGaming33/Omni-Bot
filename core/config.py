import discord
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") # Replace with .env later.
GUILD_ID = discord.Object(id=1420885374758293616) #The testing server id.