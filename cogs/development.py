import discord
from discord.ext import commands
from discord import app_commands

from core.config import DEVS

class Development(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    development = app_commands.Group(name="development", description="A collection of development commands")

    @development.command(name="ping", description="Returns the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        if interaction.user.id not in DEVS:
            await interaction.response.send_message("You are not in the list of developers, so you may not use this command.", ephemeral=True)
            return
        
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"The bot's latency is {latency_ms}ms - Pong")

async def setup(bot):
    await bot.add_cog(Development(bot))