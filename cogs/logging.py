import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.add_listener(self.on_moderation)

    async def on_moderation(self, interaction: discord.Interaction, target: Optional[discord.Member], action: str, reason: Optional[str]):
        if not reason:
            reason = "N/A"

        if target is None:
            target_id = "N/A"
            target_name = "N/A"
            target_mention = "N/A"
        else:
            target_id = target.id
            target_name = target.display_name
            target_mention = target.mention

        channel = discord.utils.get(interaction.guild.channels, name="moderation-logs")

        embed = discord.Embed(
            title=f"Omni Detected Moderation",
            description=f"Omni has detected a {action} action has been executed.",
            color=0x7289da
        )
        embed.add_field(
            name=f"{action}",
            value=f"The targetted user id was ({target_id}), name: {target_name}, {target_mention}",
            inline=False
            )
        embed.add_field(
            name="Reason:",
            value=f"{reason}",
            inline=False
        )
        embed.set_footer(text=f"The moderation was requested by name: [{interaction.user.name}], id: [{interaction.user.id}]")

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logging(bot))