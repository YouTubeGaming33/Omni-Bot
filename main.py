import discord
from discord.ext import commands
from discord import app_commands

import os, asyncio

from core.config import BOT_TOKEN, GUILD_ID

intents = discord.Intents.all()

DEV_MODE = True
TOKEN = str(BOT_TOKEN)

class Omni(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    
    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"Successfully loaded Cog: {filename}")
        
        try:
            if DEV_MODE:
                self.tree.copy_global_to(guild=GUILD_ID)
                guild_synced = await self.tree.sync(guild=GUILD_ID)
                print(f"[DEV MODE] - Synced {len(guild_synced)} Group(s) to the Development Guild.")
            else:
                global_synced = await self.tree.sync()
                print(f"[PROD MODE] - Synced {len(global_synced)} Global Group(s).")
        except Exception as e:
            print(f"Failed to sync commands: {e}")
        
bot = Omni()

async def update_activity():
    server_count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"over {server_count} servers 👀."
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.event
async def on_ready():
    await update_activity()
    print(f"Logged on as {bot.user}")

@bot.event
async def on_guild_join(guild):
    await update_activity()

@bot.event
async def on_guild_remove(guild):
    await update_activity()

async def main():
    async with bot:
        await bot.start(TOKEN)
        
asyncio.run(main())