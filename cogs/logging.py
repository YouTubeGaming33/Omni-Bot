import discord
from discord.ext import commands
from typing import Optional

def logBuilder(moderator: discord.Member, target: discord.Member, action: str, reason: str, guild: discord.Guild, caseNum: str):
    embed = discord.Embed(title=f"User {action}",description=
                          f"**User:** {target.display_name} | {target.id}\n"
                          f"**Moderator:** {moderator.display_name} | {moderator.id}\n"
                          f"**Reason:** {reason if reason else "N/A"}\n"
                          f"**Case Number:** {caseNum}",
                          colour=discord.Colour.orange())
    embed.set_thumbnail(url=target.display_avatar.url)

    if guild.icon:
        embed.set_footer(text=guild.name, icon_url=guild.icon.url)
    else:
        embed.set_footer(text=guild.name)

    return embed


class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.add_listener(self.on_moderation)

    async def on_moderation(self,interaction: discord.Interaction, target: Optional[discord.Member], action: str, reason: Optional[str], guild: discord.Guild, caseNum: str):
        channel = discord.utils.get(interaction.guild.channels, name="moderation-logs")
        if not channel:
            return  # No moderation-logs channel found
        
        embed = logBuilder(interaction.user, target, action, reason, guild, caseNum)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logging(bot))
